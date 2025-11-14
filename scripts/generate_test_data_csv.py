"""
generate_test_data_csv.py
Create CSV files for NG_Lead__c and NG_Opportunity__c test data suitable for import.

Outputs:
 - data_exports/ng_leads.csv
 - data_exports/ng_opportunities.csv

Usage:
    python .\scripts\generate_test_data_csv.py

The Opportunities CSV includes a `NG_Lead_Email__c` column to help map
opportunities to leads by email. Import Leads first, then map Opportunities
by replacing the `NG_Lead_Email__c` values with Lead IDs (or use an
external-id mapping if available).

This script does not connect to Salesforce; it only generates CSV files.
"""
import os
import csv
import datetime


DATA_DIR = os.path.join(os.path.dirname(__file__), '..', 'data_exports')


def make_dirs():
    os.makedirs(DATA_DIR, exist_ok=True)


def generate_leads():
    # Columns correspond to fields in NG_Lead__c
    headers = ['Name', 'Email__c', 'Phone__c', 'Status__c', 'Product_Interest__c']
    rows = [
        # Missing email (to exercise validation when importing)
        ['Test User No Email', '', '', 'New', 'Product A'],
        # Normal lead (unique email)
        ['Test User', 'test@test.com', '', 'New', 'Product B'],
        # Duplicate email (to exercise unique constraint)
        ['Test User Duplicate', 'test@test.com', '', 'New', 'Product B'],
        # A lead that will be converted; include phone to satisfy validation
        ['Converted Lead With Phone', 'converted_with_phone@test.com', '555-0100', 'Converted', 'Product C'],
        # Another regular lead
        ['Sales Prospect', 'prospect@example.com', '555-0200', 'New', 'Product D'],
    ]

    path = os.path.join(DATA_DIR, 'ng_leads.csv')
    with open(path, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(headers)
        writer.writerows(rows)

    return path


def generate_opportunities():
    # Columns correspond to fields in NG_Opportunity__c; use External ID format
    # NG_Lead__r.Email__c to reference leads by their Email external ID
    headers = ['Deal_Name__c', 'Amount__c', 'Stage__c', 'Close_Date__c', 'NG_Lead__r.Email__c']
    close_date = (datetime.date.today() + datetime.timedelta(days=30)).isoformat()

    rows = [
        ['Test Opportunity 1', '1000.00', 'Discovery', close_date, 'test@test.com'],
        ['Converted Lead Opportunity', '2500.00', 'Proposal', close_date, 'converted_with_phone@test.com'],
        ['Prospect Opportunity', '500.00', 'Discovery', close_date, 'prospect@example.com'],
    ]

    path = os.path.join(DATA_DIR, 'ng_opportunities.csv')
    with open(path, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(headers)
        writer.writerows(rows)

    return path


def main():
    make_dirs()
    leads_path = generate_leads()
    opps_path = generate_opportunities()
    print('Generated CSV files:')
    print(' -', os.path.abspath(leads_path))
    print(' -', os.path.abspath(opps_path))


if __name__ == '__main__':
    main()
