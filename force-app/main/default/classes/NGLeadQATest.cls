@isTest
public class NGLeadQATest {
    
    // Test Script 1: Data Integrity - Required Email Field
    @isTest
    static void testEmailRequiredValidation() {
        NG_Lead__c lead = new NG_Lead__c(
            Name = 'Test User'
            // Email intentionally left blank
        );
        
        try {
            insert lead;
            System.assert(false, 'Expected DML exception for missing required Email field');
        } catch (DmlException e) {
            System.assert(e.getMessage().contains('REQUIRED_FIELD_MISSING'), 'Expected required field error');
        }
    }
    
    // Test Script 1: Data Integrity - Unique Email Constraint
    @isTest
    static void testEmailUniqueConstraint() {
        // Create first lead with email
        NG_Lead__c lead1 = new NG_Lead__c(
            Name = 'Test User',
            Email__c = 'test@test.com',
            Status__c = 'New'
        );
        insert lead1;
        
        // Attempt to create second lead with same email
        NG_Lead__c lead2 = new NG_Lead__c(
            Name = 'Test User 2',
            Email__c = 'test@test.com',
            Status__c = 'New'
        );
        
        try {
            insert lead2;
            System.assert(false, 'Expected DML exception for duplicate email');
        } catch (DmlException e) {
            System.assert(e.getMessage().contains('DUPLICATE') || e.getMessage().contains('duplicate'), 
                'Expected duplicate error for unique email constraint');
        }
    }
    
    // Test Script 2: Business Logic - Phone Required for Conversion
    @isTest
    static void testPhoneRequiredForConversion() {
        // Create lead without phone
        NG_Lead__c lead = new NG_Lead__c(
            Name = 'Test User',
            Email__c = 'testuser@test.com',
            Status__c = 'New'
        );
        insert lead;
        
        // Attempt to convert without phone
        lead.Status__c = 'Converted';
        
        try {
            update lead;
            System.assert(false, 'Expected validation rule to fire for missing phone on conversion');
        } catch (DmlException e) {
            System.assert(e.getMessage().contains('Phone Number') || e.getMessage().contains('Phone'), 
                'Expected phone validation error');
        }
        
        // Add phone and convert successfully
        lead.Phone__c = '555-1234';
        lead.Status__c = 'Converted';
        update lead;
        
        NG_Lead__c updatedLead = [SELECT Status__c, Phone__c FROM NG_Lead__c WHERE Id = :lead.Id];
        System.assertEquals('Converted', updatedLead.Status__c);
        System.assertEquals('555-1234', updatedLead.Phone__c);
    }
    
    // Test Script 3: Relationship - Opportunity Linked to Lead
    @isTest
    static void testOpportunityLeadRelationship() {
        // Create lead
        NG_Lead__c lead = new NG_Lead__c(
            Name = 'Test User',
            Email__c = 'relationship@test.com',
            Phone__c = '555-5678',
            Status__c = 'New'
        );
        insert lead;
        
        // Create opportunity linked to lead
        NG_Opportunity__c opp = new NG_Opportunity__c(
            Deal_Name__c = 'Test Opportunity',
            Amount__c = 5000.00,
            Stage__c = 'Discovery',
            Close_Date__c = Date.today().addDays(30),
            NG_Lead__c = lead.Id
        );
        insert opp;
        
        // Verify relationship
        NG_Opportunity__c insertedOpp = [SELECT Id, NG_Lead__c FROM NG_Opportunity__c WHERE Id = :opp.Id];
        System.assertEquals(lead.Id, insertedOpp.NG_Lead__c, 'Opportunity should be linked to the Lead');
        
        // Query through relationship
        List<NG_Opportunity__c> relatedOpps = [SELECT Id FROM NG_Opportunity__c WHERE NG_Lead__c = :lead.Id];
        System.assertEquals(1, relatedOpps.size(), 'Lead should have one related opportunity');
    }
}