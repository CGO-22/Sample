

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



3. **Add watchers Rule**

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

4. **test copy featur upon update- Cpy product & feature select field value to Product_feature cas field**

        def issueKey = issue.key
        def result = get('/rest/api/2/issue/' + issueKey)
                .header('Content-Type', 'application/json')
                .asObject(Map)
        
        if (result.status == 200){
            def parentValue = result.body.fields.customfield_10112?.value
            def childValue = result.body.fields.customfield_10113?.value
            
            def bodyContent = [
                fields: [
                    customfield_10111: [
                        value: parentValue
                    ]
                ]
            ]
            
            if (childValue) {
                bodyContent.fields.customfield_10111.child = [value: childValue]
            }
            
            def result1 = put('/rest/api/2/issue/' + issueKey)
                    .header('Content-Type', 'application/json')
                    .body(bodyContent)
                    .asString()
        
            if (result1.status == 204){
                return "Issue updated successfully"
            } else {
                return "Failed to update issue: Status: ${result1.status} ${result1.body}"
            }
        } else {
            return "Failed to find issue: Status: ${result.status} ${result.body}"
        }

6. 








