global class GoogleRegistrationHandler implements Auth.RegistrationHandler {

    global User createUser(Id portalId, Auth.UserData data) {
        // Step 1: Find or create an Account for external users
        Account acc = [SELECT Id FROM Account LIMIT 1];
        if (acc == null) {
            acc = new Account(Name = 'Community External Users');
            insert acc;
        }

        // Step 2: Find or create a Contact linked to this external account
        Contact c;
        List<Contact> existingContacts = [SELECT Id,firstname,lastname FROM Contact WHERE Email = :data.email LIMIT 1];
        if (!existingContacts.isEmpty()) {
            c = existingContacts[0];
        } else {
            c = new Contact(
                FirstName = data.firstName != null ? data.firstName : 'Google',
                LastName  = data.lastName  != null ? data.lastName  : 'User',
                Email     = data.email != null ? data.email : 'noemail+' + System.currentTimeMillis() + '@example.com',
                AccountId = acc.Id
            );
            insert c;
        }

        // Step 3: Pick Customer Community Plus profile
        Id profileId = [SELECT Id FROM Profile WHERE UserLicense.Name = 'Customer Community Plus' LIMIT 1].Id;

        // Step 4: Create the external user linked to the Contact
        User u = new User();
        u.Username = (data.email != null ? data.email : 'googleuser') + '.' + String.valueOf(System.currentTimeMillis() +   '@example.com');
        u.Email = data.email != null ? data.email : 'noemail+' + String.valueOf(System.currentTimeMillis()) + '@example.com';
        u.FirstName = c.FirstName;
        u.LastName  = c.LastName;
        u.Alias = (u.FirstName.substring(0,1) + u.LastName.substring(0,2)).toLowerCase();
        //u.CommunityNickname = u.FirstName + u.LastName + System.currentTimeMillis();
        u.TimeZoneSidKey = 'Asia/Kolkata';
        u.LocaleSidKey = 'en_IN';
        u.EmailEncodingKey = 'UTF-8';
        u.LanguageLocaleKey = 'en_US';
        u.ProfileId = profileId; // ✅ Customer Community Plus profile
        u.ContactId = c.Id;      // 🔑 Mandatory for community users

        return u;
    }

    global void updateUser(Id userId, Id portalId, Auth.UserData data) {
        User u = [SELECT Id, Email, FirstName, LastName FROM User WHERE Id = :userId];
        if (data.email != null) {
            u.Email = data.email;
        }
        if (data.firstName != null) {
            u.FirstName = data.firstName;
        }
        if (data.lastName != null) {
            u.LastName = data.lastName;
        }
        update u;
    }
}