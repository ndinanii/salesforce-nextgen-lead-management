"""
Script: create_test_data.py
Purpose: Create test data in a Salesforce org to simulate "lead leakage" business problems
and validate the solution (validation rules, unique constraints, relationships).

Requirements:
- Python 3.8+
- Install dependency: pip install simple-salesforce

Authentication options (set environment variables):
1) Username/password+
   SF_USERNAME, SF_PASSWORD, SF_SECURITY_TOKEN, optional SF_DOMAIN (login.salesforce.com or test)
2) Session token (from sfdx or OAuth):
   SF_ACCESS_TOKEN and SF_INSTANCE_URL

Usage (PowerShell):
$env:SF_USERNAME = 'me@example.com'
$env:SF_PASSWORD = 'mypassword'
$env:SF_SECURITY_TOKEN = 'mytoken'
python .\scripts\create_test_data.py

Or with access token:
$env:SF_ACCESS_TOKEN = '<token>'
$env:SF_INSTANCE_URL = 'https://yourInstance.my.salesforce.com'
python .\scripts\create_test_data.py

The script will:
- Attempt to create a Lead without email (expect required-field error)
- Create a Lead with email
- Attempt to create a duplicate Lead with same email (expect unique constraint error)
- Attempt to convert the Lead without phone (expect validation rule to block)
- Add phone and convert successfully
- Create an Opportunity linked to the Lead and verify relationship

"""

import os
import sys
import datetime

from simple_salesforce import Salesforce, SalesforceMalformedRequest, SalesforceResourceNotFound, SalesforceAuthenticationFailed


def connect():
    access_token = os.getenv('SF_ACCESS_TOKEN')
    instance_url = os.getenv('SF_INSTANCE_URL')
    if access_token and instance_url:
        print('Connecting using session token...')
        return Salesforce(instance_url=instance_url, session_id=access_token)

    username = os.getenv('SF_USERNAME')
    password = os.getenv('SF_PASSWORD')
    token = os.getenv('SF_SECURITY_TOKEN')
    domain = os.getenv('SF_DOMAIN') or 'login'

    if not (username and password and token):
        print('ERROR: set SF_USERNAME, SF_PASSWORD and SF_SECURITY_TOKEN, or SF_ACCESS_TOKEN+SF_INSTANCE_URL')
        sys.exit(2)

    try:
        print('Connecting using username/password...')
        sf = Salesforce(username=username, password=password, security_token=token, domain=domain)
        print(f'Connected to: {sf.sf_instance}')
        return sf
    except SalesforceAuthenticationFailed as e:
        print('Authentication failed:', e)
        sys.exit(2)


def create_lead(sf, lead_data):
    try:
        res = sf.NG_Lead__c.create(lead_data)
        print('Created Lead:', res['id'])
        return res['id']
    except SalesforceMalformedRequest as e:
        print('Create Lead failed:', e.content if hasattr(e, 'content') else e)
        return None


def update_lead(sf, lead_id, fields):
    try:
        sf.NG_Lead__c.update(lead_id, fields)
        print(f'Updated Lead {lead_id} with {fields}')
        return True
    except SalesforceMalformedRequest as e:
        print('Update Lead failed:', e.content if hasattr(e, 'content') else e)
        return False


def create_opportunity(sf, opp_data):
    try:
        res = sf.NG_Opportunity__c.create(opp_data)
        print('Created Opportunity:', res['id'])
        return res['id']
    except SalesforceMalformedRequest as e:
        print('Create Opportunity failed:', e.content if hasattr(e, 'content') else e)
        return None


def run():
    sf = connect()

    print('\n=== Test Script 1: Data Integrity ===')
    print('\n1. Create Lead without Email (expect failure)')
    lead_no_email = {'Name': 'Test User', 'Status__c': 'New'}
    id1 = create_lead(sf, lead_no_email)
    if not id1:
        print('As expected, lead creation without Email failed.')
    else:
        print('Unexpected: lead created without Email:', id1)

    print('\n2. Create Lead with Email test@test.com (expect success)')
    lead_ok = {'Name': 'Test User', 'Email__c': 'test@test.com', 'Status__c': 'New'}
    lead_id = create_lead(sf, lead_ok)
    if not lead_id:
        print('Failed to create the initial lead, cannot continue tests.')
        return

    print('\n3. Create duplicate Lead with same email (expect unique constraint failure)')
    lead_dup = {'Name': 'Test User Duplicate', 'Email__c': 'test@test.com', 'Status__c': 'New'}
    dup_id = create_lead(sf, lead_dup)
    if not dup_id:
        print('As expected, duplicate lead creation failed.')
    else:
        print('Unexpected: duplicate lead created:', dup_id)

    print('\n=== Test Script 2: Business Logic ===')
    print('\n1. Attempt to convert the lead without Phone (expect validation rule to block)')
    success = update_lead(sf, lead_id, {'Status__c': 'Converted'})
    if not success:
        print('Validation rule prevented conversion as expected.')
    else:
        print('Unexpected: Lead converted without phone (validation may not be active in org).')

    print('\n2. Add Phone and convert (expect success)')
    added = update_lead(sf, lead_id, {'Phone__c': '555-0100'})
    if not added:
        print('Failed to add phone to lead, aborting conversion test.')
    else:
        converted = update_lead(sf, lead_id, {'Status__c': 'Converted'})
        if converted:
            print('Lead converted successfully after adding phone.')
        else:
            print('Conversion still blocked. Check validation rules and triggers.')

    print('\n=== Test Script 3: Relationship ===')
    print('\n1. Create Opportunity linked to the lead')
    opp = {
        'Deal_Name__c': 'Test Opportunity',
        'Amount__c': 1000.00,
        'Stage__c': 'Discovery',
        'Close_Date__c': (datetime.date.today() + datetime.timedelta(days=30)).isoformat(),
        'NG_Lead__c': lead_id
    }
    opp_id = create_opportunity(sf, opp)
    if opp_id:
        print('Opportunity created and linked to Lead:', opp_id)
    else:
        print('Failed to create linked Opportunity. Please verify lookup field and metadata.')

    print('\nDone.')


if __name__ == '__main__':
    run()
