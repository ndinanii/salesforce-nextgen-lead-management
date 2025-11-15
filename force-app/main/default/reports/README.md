# NextGen Lead Reports

This folder contains report metadata for the NextGen Lead Management system.

## Report: Opportunities from Converted Leads

**Status**: Create this report manually in your Salesforce org using the instructions below.

**Folder**: NextGen Lead Reports ✅ (Deployed)
**Report Type**: NextGen Leads with Opportunities ✅ (Deployed)

---

### Step-by-Step Instructions to Create the Report

1. **Navigate to Reports**
   - Click on the **Reports** tab in Salesforce

2. **Create New Report**
   - Click **New Report** button
   - Search for and select: **NextGen Leads with Opportunities**
   - Click **Start Report**

3. **Add Filter**
   - Click **Add filter...**
   - Select **Lead: Status**
   - Operator: **equals**
   - Value: **Converted**
   - Click **Apply**

4. **Add Columns** (if not already visible)
   - **Lead: Name** (should be included by default)
   - **Lead: Email**
   - **Lead: Phone**
   - **Lead: Product Interest**
   - **Opportunity: Deal Name**
   - **Opportunity: Amount**
   - **Opportunity: Stage**
   - **Opportunity: Close Date**

5. **Configure Grouping**
   - Click **Add group...**
   - **Primary Grouping**: Lead: Status
   - Click **Add group...**  again
   - **Secondary Grouping**: Opportunity: Stage

6. **Add Summaries**
   - For **Opportunity: Amount** column:
     - Click the dropdown arrow on the column header
     - Select **Summarize** → **Sum**
   - The report will automatically show **Record Count** in groupings

7. **Save the Report**
   - Click **Save**
   - **Report Name**: Opportunities from Converted Leads
   - **Report Description**: Shows all opportunities created from converted leads, enabling sales managers to track conversion rates, calculate total pipeline value, analyze revenue sources, and identify bottlenecks in the sales process.
   - **Report Folder**: NextGen Lead Reports
   - Click **Save**

---

### What This Report Shows

- **All converted leads** with their associated opportunities
- **Total pipeline value** from converted leads (sum of all opportunity amounts)
- **Opportunity counts** by status and stage
- **Revenue tracking** from lead source to closed deals
- **Sales process bottlenecks** (stages where opportunities get stuck)

### Business Value

✅ **Track Conversion Rates**: See which leads successfully convert to opportunities  
✅ **Calculate Pipeline Value**: Total revenue potential from converted leads  
✅ **Analyze Revenue Sources**: Identify which lead sources generate the most revenue  
✅ **Identify Bottlenecks**: Spot where deals get stuck in the sales process

---

## Report Deployed Successfully? ✅

Once you've created the report manually, you can verify:
- [ ] Report appears in NextGen Lead Reports folder
- [ ] Filter shows only Converted leads
- [ ] All 8 columns are visible
- [ ] Grouped by Status and Stage
- [ ] Sum of Amount shows total pipeline value
- [ ] Can run report and see data

---

**Note**: Reports with complex groupings and summaries are best created through the Salesforce UI rather than deployed as metadata files, as the UI ensures proper field references and summary calculations.
