@isTest
public class NGLeadTest {
    @isTest
    static void testNGLeadFunctionality() {
        // Create a test NextGen Lead record
        NG_Lead__c lead = new NG_Lead__c(
            Name = 'John Doe',
            Email__c = 'john.doe@example.com',
            Phone__c = '123-456-7890',
            Status__c = 'New',
            Product_Interest__c = 'TV'
        );
        insert lead;

        // Verify the record was inserted
        NG_Lead__c insertedLead = [SELECT Id, Name, Email__c, Phone__c, Status__c, Product_Interest__c FROM NG_Lead__c WHERE Id = :lead.Id];
        System.assertEquals('John Doe', insertedLead.Name);
        System.assertEquals('john.doe@example.com', insertedLead.Email__c);
        System.assertEquals('123-456-7890', insertedLead.Phone__c);
        System.assertEquals('New', insertedLead.Status__c);
        System.assertEquals('TV', insertedLead.Product_Interest__c);

        // Update the lead status
        insertedLead.Status__c = 'Contacted';
        update insertedLead;

        // Verify the status was updated
        NG_Lead__c updatedLead = [SELECT Id, Status__c FROM NG_Lead__c WHERE Id = :lead.Id];
        System.assertEquals('Contacted', updatedLead.Status__c);

        // Delete the lead
        delete lead;

        // Verify the record was deleted
        Integer count = [SELECT COUNT() FROM NG_Lead__c WHERE Id = :lead.Id];
        System.assertEquals(0, count);
    }
}