

1. **Automatically close TM Alerts**
    
    //Condition
    issue.customfield_10083 >= 2 && issue.customfield_10083 < 3
    
    //additional code 
    def doneTransitionId = 31
    
    def transition = post("/rest/api/2/issue/" + issue.key + "/transitions")
                .header("Content-Type", "application/json")
                .body([transition: [id: doneTransitionId]])
                .asObject(Map)
    
    assert transition.status >= 200 && transition.status <= 300



2. **Add watchers Rule**

        def issueKey =issue.key
        
        
        // Specify the account ID of the user you want to add
        def accountId = '630a0d15ec02b5f28b63a024'
        
        def watcherResp = post("/rest/api/2/issue/${issueKey}/watchers")
            .header('Content-Type', 'application/json')
            .body("\"${accountId}\"")
            .asString()
        
        if (watcherResp.status == 204) {
            logger.info("Successfully added user with account ID ${accountId} as watcher of ${issueKey}")
        } else {
            logger.error("Error adding watcher: ${watcherResp.body}")
        }










