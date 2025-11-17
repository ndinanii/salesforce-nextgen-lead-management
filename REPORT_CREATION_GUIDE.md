# Report Instructions: Opportunities from Converted Leads

## ✅ Everything is Ready - Report Type Deployed!

The custom report type **"NextGen Leads with Opportunities"** has been successfully deployed to your Salesforce org. You can now create your report.

---

## 📊 How to Create the Report in Salesforce UI

### Step 1: Navigate to Reports
1. Click on the **Reports** tab in Salesforce
2. Click **New Report**

### Step 2: Select Report Type
1. In the search box, type: **NextGen Leads with Opportunities**
2. Select it from the list
3. Click **Start Report** or **Create**

### Step 3: Add Filter for Converted Leads
1. In the Filters section, click **Add filter...**
2. Search for and select: **Lead: Status**
3. Set the operator to: **equals**
4. Enter value: **Converted**
5. Click **Apply**

### Step 4: Select Columns to Display
The report should already show these columns (if not, add them):

**Lead Information:**
- Lead Name
- Email
- Phone
- Status
- Product Interest

**Opportunity Information:**
- Opportunity Name (or Deal Name)
- Amount
- Stage
- Close Date

### Step 5: Add Grouping (Optional but Recommended)
1. Click **Add group...**
2. **First grouping**: Select **Lead: Status**
3. Click **Add group...** again
4. **Second grouping**: Select **Opportunity: Stage**

### Step 6: Add Summary Calculations
1. Find the **Amount** column
2. Click the dropdown arrow (▼) on the column header
3. Select **Summarize** → **Sum**
4. This will calculate total pipeline value from converted leads

### Step 7: Save the Report
1. Click **Save** or **Save & Run**
2. **Report Name**: `Opportunities from Converted Leads`
3. **Report Description**: `Shows all opportunities created from converted leads for tracking conversion rates and pipeline value`
4. **Report Folder**: Select **NextGen Lead Reports**
5. Click **Save**

---

## 🎯 What This Report Will Show You

✅ **All converted leads** with their associated opportunities  
✅ **Total pipeline value** from converted leads (sum of all opportunity amounts)  
✅ **Conversion tracking** - which leads turned into real sales opportunities  
✅ **Revenue potential** - see how much money is in the pipeline from each lead  
✅ **Sales stage visibility** - where each opportunity is in the sales process  

---

## 💡 Business Value

This report helps you:
- **Track conversion rates**: What % of leads become opportunities?
- **Measure marketing ROI**: Which lead sources generate revenue?
- **Forecast revenue**: Total value of opportunities from converted leads
- **Identify bottlenecks**: Which stages are opportunities getting stuck in?
- **Optimize sales process**: See the full lead-to-revenue journey

---

## 🔍 Sample Questions This Report Answers

1. How many opportunities were created from converted leads this month?
2. What's the total potential revenue from converted leads?
3. Which product interests generate the most opportunity value?
4. What's the average deal size from converted leads?
5. How many converted leads resulted in closed-won deals?

---

## ✅ Pre-Deployment Checklist (COMPLETED)

- ✅ Report Type: **NextGen Leads with Opportunities** - Deployed
- ✅ Report Folder: **NextGen Lead Reports** - Created
- ✅ Relationship: **Primary_Lead_Opportunities__r** - Configured
- ✅ Required Fields: **Status__c, Close_Date__c** - Marked as required
- ✅ All metadata committed to GitHub

---

**You're all set!** Just follow the steps above to create your report in the Salesforce UI.
