# Report Types

Report types should be created manually in Salesforce Setup UI to ensure proper field relationships and metadata structure.

## Assessment Requirement #8: Create Custom Report Type

**Instructions for creating the report type manually:**

1. Go to **Setup** → **Report Types** → **New Custom Report Type**
2. **Primary Object**: NextGen Leads (NG_Lead__c)
3. **Report Type Label**: NextGen Leads with Opportunities
4. **Description**: Shows NextGen Leads with their related Opportunities
5. **Category**: Other Reports
6. **Deployment Status**: Deployed
7. Click **Next**
8. You'll see "A: NextGen Leads" box
9. Below it, click **"Click to relate another object"**
10. Select: **NextGen Opportunities** (will appear via Primary_Lead_Opportunities relationship)
11. Relationship type: **"Each 'A' record must have at least one related 'B' record"** (Inner Join)
12. Click **Save**

This creates a report type that shows Leads with their related Opportunities, enabling you to create reports showing opportunities from converted leads.

---

**Why create manually?**
- Ensures proper relationship mapping in Salesforce
- Avoids metadata API relationship name conflicts
- UI validates all field references automatically
- Provides immediate visual feedback on available fields
