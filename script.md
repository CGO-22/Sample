

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

3. **test copy featur upon update- Cpy product & feature select field value to Product_feature cas field**

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
4. **when an issue is created --> automatically assign using Round Robin**

    **create proprties using Curl**
   
        curl -X PUT 'https://stagingproject.atlassian.net/rest/api/3/project/USE/properties/round-robbin' --user 'charanv@devtools.in:<token>' -H 'Accept: application/json' -H 'Content-Type: application/json' -d '{
                "value": {
                  "lastIndex": 0
                }
              }'


    **Retrieve current value of round-robin project property**
   
            def result = get("/rest/api/2/project/<projectkey>/properties/round-robin")asString().body
            def parsedJson = new groovy.json.JsonSlurper().parseText(result)
            def lastIndex = parsedJson.value.lastIndex
            
            // Define account IDs of users to be assigned issues
            def users = ['accountID1','accountID2']
            
            // Define issue key variable
            def issueKey = issue.key;
            
            // Update issue with next assignee based on round-robin index and users array
            def assignIssue = put("rest/api/2/issue/${issueKey}")
                    .header('Content-Type', 'application/json')
                    .queryString("notifyUsers":false)
                    .body([
                    fields:[
                            assignee: [id:users[lastIndex]]
                    ]
            ])
                    .asString()
            if (assignIssue.status == 204) {
                // Update the index for the next user assignment
                lastIndex = (lastIndex + 1) % users.size()
                
                // Update the round-robin project property value
                def updateroundrobin = put("/rest/api/2/project/<projectkey>/properties/round-robin")
                    .header('Content-Type', 'application/json')
                    .header('Accept', 'application/json')
                    .body(["lastIndex": lastIndex])
                    .asString()
                    
                return 'Success'
            } else {
                return "${assignIssue.status}: ${assignIssue.body}"

      }

   
5. **Send email when new ticket created**

            def issueKey = issue.key
            def result = get('/rest/api/2/issue/' + issueKey)
                    .header('Content-Type', 'application/json')
                    .asObject(Map)
            if (result.status == 200){
                    def resp = post("/rest/api/2/issue/${issueKey}/notify")
                        .header("Content-Type", "application/json")
                        .body([
                            "subject": "Issue " + issueKey + " has been updated",
                            "textBody": result.body.fields.summary,
                            "to": [
                                "users": [
                                    [
                                        "emailAddress": "charanv@devtools.in"
                                    ]
                                ]
                            ]
                        ])
                        .asString()
                
                    return resp
            } else {
                return "Failed to find issue: Status: ${result.status} ${result.body}"
            }

 6. **Ticket End time Update FS**

            def outputCfId = 'customfield_10054'
            def currentTime = new Date().format("yyyy-MM-dd'T'HH:mm:ss.SSSZ") // Adjust the format as needed
            def output = currentTime
             
            put("/rest/api/2/issue/${issue.key}") 
                .header("Content-Type", "application/json")
                .body([
                    fields:[
                        (outputCfId): output
                    ]
                ])
                .asString()
    
7.  **copy product value for subtasks**

            def issueKey = issue.key

            def result = get('/rest/api/2/issue/' + issueKey)
                    .header('Content-Type', 'application/json')
                    .asObject(Map)
            if (result.status == 200){
                print("created")
            } else {
               print("Failed to find issue: Status: ${result.status} ${result.body}")
            }
            
             if(result.body.fields.issuetype.name == "Sub-task")   {
                def parent = result.body.fields.parent.key
                
                def result1 = get('/rest/api/2/issue/' + parent)
                        .header('Content-Type', 'application/json')
                        .asObject(Map)
                if (result1.status == 200){
                    def parentValue = result1.body.fields.customfield_10111.value
                    def childValue = result1.body.fields.customfield_10111.child.value
                    
                    def result2 = put('/rest/api/2/issue/' + issueKey)
                        .header('Content-Type', 'application/json')
                        .body([
                                fields: [
                                        customfield_10111: [
                                                value: parentValue,
                                                child: [
                                                        value: childValue
                                                ]
                                        ]
                                ]
                        ])
                        .asString()
                    
                } else {
                   print("Failed to find issue: Status: ${result2.status} ${result2.body}")
                }
            
            
            }
            else {
                   print("Failed to find issue: Status: ${result.status} ${result.body}")
                }










