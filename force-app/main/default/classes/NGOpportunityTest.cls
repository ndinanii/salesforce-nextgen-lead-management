@isTest
public class NGOpportunityTest {
    @isTest
    static void testNGOpportunityFunctionality() {
        // Create a test NextGen Lead record to link to
        NG_Lead__c lead = new NG_Lead__c(
            Name = 'Jane Smith',
            Email__c = 'jane.smith@example.com',
            Phone__c = '555-987-6543',
            Status__c = 'New',
            Product_Interest__c = 'Computing'
        );
        insert lead;

        // Create an Opportunity linked to the lead
        NG_Opportunity__c opp = new NG_Opportunity__c(
            Deal_Name__c = 'Jane Smith - Laptop Purchase',
            Amount__c = 1200.00,
            Stage__c = 'Discovery',
            Close_Date__c = Date.today().addDays(30),
            NG_Lead__c = lead.Id
        );
        insert opp;

        // Verify the opportunity was inserted and linked
        NG_Opportunity__c insertedOpp = [SELECT Id, Deal_Name__c, Amount__c, Stage__c, Close_Date__c, NG_Lead__c FROM NG_Opportunity__c WHERE Id = :opp.Id];
        System.assertEquals('Jane Smith - Laptop Purchase', insertedOpp.Deal_Name__c);
        System.assertEquals(1200.00, insertedOpp.Amount__c);
        System.assertEquals('Discovery', insertedOpp.Stage__c);
        System.assertEquals(lead.Id, insertedOpp.NG_Lead__c);

        // Update stage
        insertedOpp.Stage__c = 'Proposal';
        update insertedOpp;

        NG_Opportunity__c updatedOpp = [SELECT Id, Stage__c FROM NG_Opportunity__c WHERE Id = :opp.Id];
        System.assertEquals('Proposal', updatedOpp.Stage__c);

        // Clean up
        delete insertedOpp;
        delete lead;

        Integer remainingOpps = [SELECT COUNT() FROM NG_Opportunity__c WHERE Id = :opp.Id];
        Integer remainingLeads = [SELECT COUNT() FROM NG_Lead__c WHERE Id = :lead.Id];
        System.assertEquals(0, remainingOpps);
        System.assertEquals(0, remainingLeads);
    }
}