"""
map_opps_to_lead_ids.py

Map opportunities in `ng_opportunities.csv` to Lead IDs by looking up
leads in Salesforce (by Email__c) or using a provided mapping CSV.

Usage examples (PowerShell):
  # Using Salesforce credentials in env vars (SF_USERNAME/SF_PASSWORD/SF_SECURITY_TOKEN or SF_ACCESS_TOKEN+SF_INSTANCE_URL):
  .\.venv\Scripts\python.exe .\scripts\map_opps_to_lead_ids.py

  # Using a mapping file (Email,Id):
  .\.venv\Scripts\python.exe .\scripts\map_opps_to_lead_ids.py --mapping .\data_exports\lead_email_id_mapping.csv

Outputs:
  - data_exports/ng_opportunities_for_import.csv (column `NG_Lead__c` with Lead IDs)

If some emails are not found, the script will leave the `NG_Lead__c` cell blank and
report warnings. You can supply a mapping CSV with headers `Email,Id` to avoid
connecting to Salesforce.
"""
import os
import csv
import argparse
import sys

try:
    from simple_salesforce import Salesforce, SalesforceAuthenticationFailed
except Exception:
    Salesforce = None


ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
DATA_DIR = os.path.join(ROOT, 'data_exports')
INPUT_DEFAULT = os.path.join(DATA_DIR, 'ng_opportunities.csv')
OUTPUT_DEFAULT = os.path.join(DATA_DIR, 'ng_opportunities_for_import.csv')


def connect_sf():
    if Salesforce is None:
        print('simple-salesforce not installed. Install with: pip install simple-salesforce')
        return None

    access_token = os.getenv('SF_ACCESS_TOKEN')
    instance_url = os.getenv('SF_INSTANCE_URL')
    if access_token and instance_url:
        print('Connecting to Salesforce using session token...')
        return Salesforce(instance_url=instance_url, session_id=access_token)

    username = os.getenv('SF_USERNAME')
    password = os.getenv('SF_PASSWORD')
    token = os.getenv('SF_SECURITY_TOKEN')
    domain = os.getenv('SF_DOMAIN') or 'login'
    if not (username and password and token):
        return None

    try:
        print('Connecting to Salesforce using username/password...')
        return Salesforce(username=username, password=password, security_token=token, domain=domain)
    except SalesforceAuthenticationFailed as e:
        print('Authentication failed:', e)
        return None


def read_mapping_file(mapping_path):
    mapping = {}
    with open(mapping_path, newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for r in reader:
            email = (r.get('Email') or r.get('email') or '').strip()
            idv = (r.get('Id') or r.get('ID') or r.get('id') or '').strip()
            if email and idv:
                mapping[email.lower()] = idv
    return mapping


def query_lead_ids(sf, emails):
    # emails: set of emails
    mapping = {}
    if not emails:
        return mapping

    # Build SOQL with properly quoted emails
    escaped = ["'{}'".format(e.replace("'", "\\'")) for e in emails]
    soql = f"SELECT Id, Email__c FROM NG_Lead__c WHERE Email__c IN ({','.join(escaped)})"
    print('Querying org for lead Ids...')
    try:
        res = sf.query_all(soql)
    except Exception as e:
        print('SOQL query failed:', e)
        return mapping

    for rec in res.get('records', []):
        email = (rec.get('Email__c') or '').strip().lower()
        if email:
            mapping[email] = rec.get('Id')
    return mapping


def map_opps(input_csv, output_csv, mapping):
    with open(input_csv, newline='', encoding='utf-8') as inf:
        reader = csv.DictReader(inf)
        rows = list(reader)
        fieldnames = list(reader.fieldnames or [])

    # Replace NG_Lead_Email__c -> NG_Lead__c
    email_col = None
    for fn in fieldnames:
        if fn.strip().lower() == 'ng_lead_email__c':
            email_col = fn
            break

    if not email_col:
        print('Input CSV does not contain NG_Lead_Email__c column. No changes made.')
        return False

    # Prepare output fields
    out_fields = [fn for fn in fieldnames if fn != email_col]
    # Insert NG_Lead__c in place of the email column
    insert_at = fieldnames.index(email_col)
    out_fields.insert(insert_at, 'NG_Lead__c')

    missing = set()
    for r in rows:
        email = (r.get(email_col) or '').strip().lower()
        lead_id = mapping.get(email)
        if not lead_id and email:
            missing.add(email)
        r['NG_Lead__c'] = lead_id or ''
        # remove original email helper column
        if email_col in r:
            del r[email_col]

    # Write output CSV
    with open(output_csv, 'w', newline='', encoding='utf-8') as outf:
        writer = csv.DictWriter(outf, fieldnames=out_fields)
        writer.writeheader()
        for r in rows:
            writer.writerow({k: r.get(k, '') for k in out_fields})

    if missing:
        print('Warning: The following lead emails were not found in mapping/org:')
        for m in sorted(missing):
            print(' -', m)
    print('Wrote mapped opportunities:', os.path.abspath(output_csv))
    return True


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--input', '-i', default=INPUT_DEFAULT, help='Path to input opportunities CSV')
    parser.add_argument('--output', '-o', default=OUTPUT_DEFAULT, help='Path to output opportunities CSV')
    parser.add_argument('--mapping', '-m', help='Path to a mapping CSV with headers Email,Id')
    parser.add_argument('--create-mapping-sample', action='store_true', help='Create a sample mapping CSV from existing ng_leads.csv for testing')
    args = parser.parse_args()

    if not os.path.exists(args.input):
        print('Input file not found:', args.input)
        sys.exit(2)

    mapping = {}
    if args.mapping:
        if not os.path.exists(args.mapping):
            print('Mapping file not found:', args.mapping)
            sys.exit(2)
        mapping = read_mapping_file(args.mapping)
        print(f'Loaded {len(mapping)} mappings from {args.mapping}')
    else:
        sf = connect_sf()
        if sf is None:
            if args.create_mapping_sample:
                # Create a sample mapping from local leads CSV (emails -> fake ids) for testing
                sample_in = os.path.join(DATA_DIR, 'ng_leads.csv')
                sample_out = os.path.join(DATA_DIR, 'lead_email_id_mapping_sample.csv')
                if os.path.exists(sample_in):
                    print('Creating sample mapping from', sample_in)
                    with open(sample_in, newline='', encoding='utf-8') as f:
                        reader = csv.DictReader(f)
                        with open(sample_out, 'w', newline='', encoding='utf-8') as fo:
                            writer = csv.writer(fo)
                            writer.writerow(['Email', 'Id'])
                            i = 1
                            for r in reader:
                                email = (r.get('Email__c') or '').strip()
                                if email:
                                    writer.writerow([email, f'00QFAKE{i:04d}'])
                                    i += 1
                    print('Sample mapping written to', sample_out)
                    mapping = read_mapping_file(sample_out)
                else:
                    print('No Salesforce credentials and no local leads file to create sample mapping.')
                    sys.exit(2)
            else:
                print('No Salesforce credentials found and no mapping file provided.')
                print('Provide SF creds via environment variables or use --mapping <file>')
                sys.exit(2)
        else:
            # Read input CSV to collect emails
            emails = set()
            with open(args.input, newline='', encoding='utf-8') as inf:
                reader = csv.DictReader(inf)
                for r in reader:
                    for k in r.keys():
                        if k.strip().lower() == 'ng_lead_email__c':
                            val = (r.get(k) or '').strip()
                            if val:
                                emails.add(val)
            mapping = query_lead_ids(sf, emails)
            print(f'Found {len(mapping)} lead ids in org')

    success = map_opps(args.input, args.output, mapping)
    if not success:
        sys.exit(2)


if __name__ == '__main__':
    main()
