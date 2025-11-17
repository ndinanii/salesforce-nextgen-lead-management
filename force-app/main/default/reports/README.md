# Reports

Reports should be created manually in Salesforce UI after creating the custom report type.

## Assessment Requirement #8: Create Report Showing Opportunities from Converted Leads

**Prerequisites:**
1. ✅ Custom report type "NextGen Leads with Opportunities" must be created first (see ../reportTypes/README.md)
2. ✅ Sample lead data imported
3. ✅ At least one lead converted to opportunity

**Instructions for creating the report manually:**

1. Go to **Reports** tab → **New Report**
2. Search for and select: **NextGen Leads with Opportunities**
3. Click **Start Report** or **Create**
4. **Add Filter**:
   - Field: Lead Status
   - Operator: equals
   - Value: Converted
   - Click Apply
5. **Select Columns** (add if not visible):
   - Lead: Name
   - Lead: Email
   - Lead: Phone  
   - Lead: Product Interest
   - Opportunity: Deal Name
   - Opportunity: Amount
   - Opportunity: Stage
   - Opportunity: Close Date
6. **Add Grouping** (optional but recommended):
   - Primary: Lead Status
   - Secondary: Opportunity Stage
7. **Add Summary**:
   - On Amount column: Click dropdown → Summarize → Sum
8. **Save Report**:
   - Name: Opportunities from Converted Leads
   - Description: Shows all opportunities created from converted leads
   - Folder: Create new folder "NextGen Lead Reports" or use existing

---

**What this report shows:**
- All opportunities linked to converted leads
- Total pipeline value from converted leads
- Breakdown by opportunity stage
- Lead source and product interest for each opportunity

**Business Value:**
- Track conversion rates (leads → opportunities)
- Measure total revenue potential from lead pipeline
- Identify which lead sources generate the most opportunity value
- Spot bottlenecks in the sales process
