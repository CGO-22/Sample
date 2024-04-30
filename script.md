

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


8. **Assign unassigned defects** 

        def issueKey = issue.key
        def result = get('/rest/api/2/issue/' + issueKey)
                .header('Content-Type', 'application/json')
                .asObject(Map)
        if (result.body.fields.assign == null && result.body.fields.issuetype.name == 'Bug'){
        
        def result2 = put('/rest/api/2/issue/' + issueKey)
                    .header('Content-Type', 'application/json')
                    .body([
                            fields: [
                                    assignee : [
                                          id: '630a0d15ec02b5f28b63a024'
                                     ],
                                    
                            ]
                    ])
                    .asString()
       
    } else {
        return "Failed to find issue: Status: ${result.status} ${result.body}"
    }

9. **Sub task automatic transition**

        // Define transition IDs for different statuses
        def todoTransitionId = 11
        def inProgressTransitionId = 21
        def doneTransitionId = 31
        
        // Check the current status of the parent issue
        def parentStatus = issue.fields.status.name
        
        // Map parent statuses to corresponding subtask transition IDs
        def transitionMap = [
            "To Do": todoTransitionId,
            "In Progress": inProgressTransitionId,
            "Done": doneTransitionId
        ]
        
        // Get the transition ID for the parent status
        def transitionId = transitionMap[parentStatus]
        
        // Transition subtasks based on the parent status
        transitionSubtasks(transitionId)
        
        // Function to transition subtasks
        def transitionSubtasks(transitionId) {
            // Get all subtasks below the parent issue
            def jqlQuery = "parent=${issue.key}"
            def allSubTasks = get("/rest/api/2/search")
                    .queryString("jql", jqlQuery)
                    .asObject(Map)
        
            assert allSubTasks.status >= 200 && allSubTasks.status <= 300
        
            def subtaskIssues = allSubTasks.body.issues as List<Map>
        
            // Iterate over each subtask and transition
            subtaskIssues.each { subtask ->
                def transition = post("/rest/api/2/issue/" + subtask.key + "/transitions")
                        .header("Content-Type", "application/json")
                        .body([transition: [id: transitionId]])
                        .asObject(Map)
        
                assert transition.status >= 200 && transition.status <= 300
            }
        }

10. **Send mail to Single user picker field user**

        def issueKey = issue.key

        def result = get('/rest/api/2/issue/' + issueKey)
                .header('Content-Type', 'application/json')
                .asObject(Map)
        if (result.status == 200){
           
        
            def id = result.body.fields.customfield_10057?.accountId
        
            def resp = post("/rest/api/2/issue/${issueKey}/notify")
                .header("Content-Type", "application/json")
                .body([
                    "subject": "Issue " + issueKey + " has been updated",
                    "textBody": result.body.fields.summary,
                    "to": [
                        "users": [
                            [
                                "accountId": id
                            ]
                        ]
                    ]
                ])
                .asString()
        
            return resp
        } else {
            return "Failed to find issue: Status: ${result.status} ${result.body}"
        }

11. **if all child issues "in progres" then it parent transition to "in progres"**

        def issueKey = issue.key
        def transitionId = 21
        
        // Retrieve the issue
        def issueResult = get("/rest/api/2/issue/${issueKey}")
                .header('Content-Type', 'application/json')
                .asObject(Map)
        
        if (issueResult.status != 200) {
             logger.warn("Failed to find issue: Status: ${issueResult.status} ${issueResult.body}")
        }
        
        def parentKey = issueResult.body.fields?.parent?.key
        
        if (!parentKey) {
            logger.warn("Parent issue not found for ${issueKey}")
        }
        
        // Retrieve all child issues
        def childIssuesResult = get("/rest/api/2/search")
                .queryString("jql", "parent=${parentKey}")
                .asObject(Map)
        
        assert childIssuesResult.status >= 200 && childIssuesResult.status <= 300
        
        def childIssues = childIssuesResult.body.issues as List<Map>
        
        // Check if all child issues are "In Progress"
        def allInProgress = childIssues.every { child ->
            def childResult = get("/rest/api/2/issue/${child.key}")
                    .header('Content-Type', 'application/json')
                    .asObject(Map)
        
            if (childResult.status == 200) {
                return childResult.body.fields.status.name == "In Progress"
            } else {
                return false
            }
        }
        
        if (allInProgress) {
            // Transition the parent issue
            def transition = post("/rest/api/2/issue/${parentKey}/transitions")
                    .header("Content-Type", "application/json")
                    .body([transition: [id: transitionId]])
                    .asObject(Map)
        } else {
             logger.warn("Not all child issues are in progress.")
        }

12. **When issue transitioned send the slack message**

    
        def issueKey = issue.key
        def jiraResult = get("/rest/api/2/issue/${issueKey}")
                .header('Content-Type', 'application/json')
                .asObject(Map)
        if (jiraResult.status == 200){
        def jiraFields = jiraResult.body.fields
        
        def webhookUrl = 'https://hooks.slack.com/services/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'
    
        def msg = [
            text: "${issueKey} Updated"
        ]
    
        post(webhookUrl)
            .header('Content-Type', 'application/json')
            .body(msg)
            .asString()
        } else {
        println "Failed to find issue: Status: ${jiraResult.status} ${jiraResult.body}"
        }

13. **Inherit PAF fields for subtasks from its parent**

        def issueKey = 'SR-26'
    
        def result = get('/rest/api/2/issue/' + issueKey)
                .header('Content-Type', 'application/json')
                .asObject(Map)
        if (result.status == 200){
            logger.warn("Success")
        } else {
            return "Failed to find issue: Status: ${result.status} ${result.body}"
        }
        
        def parent = result.body.fields.parent.key
        logger.warn("Parent issue key: $parent")
        
        def result2 = get('/rest/api/2/issue/' + parent)
                .header('Content-Type', 'application/json')
                .asObject(Map)
        
        def product = result2.body.fields.customfield_10112?.value
        def feature = result2.body.fields.customfield_10113?.value
        
        logger.warn("Product: $product")
        logger.warn("Feature: $feature")
        
        def result3 = put('/rest/api/2/issue/' + issueKey)
                     .header('Content-Type', 'application/json')
                     .body([
                             fields: [
                                     customfield_10112: [
                                                value: product
                                     ],
                                     customfield_10113: [
                                                value: feature
                                     ]
                             ]
                     ])
                     .asString()
        
        if (result3.status == 204) {
            logger.warn("Issue update successful")
        } else {
            logger.warn("Issue update failed: Status: ${result3.status} ${result3.body}")
        }

14. **Alert on new item added to a started sprint for PS**

        def issueKey = issue.key
        def customFieldToMonitor = "customfield_10020"
        
        // Get the changelog for the issue
        def changelogResponse = get('/rest/api/3/issue/' + issueKey + '/changelog?orderBy=-created')
                                .header('Content-Type', 'application/json')
                                .asObject(Map)
        
        // Check if the request was successful
        if (changelogResponse.status != 200) {
           logger.error("Failed to fetch changelog for issue $issueKey. Status code: ${changelogResponse.status}")
           return;
        }
        
        // Extract the changelog entries
        def changelog = changelogResponse.body.values
        
        // Iterate through changelog entries and extract 'created' and 'items' values
        def createdAndItemsValues = changelog.collect { entry ->
            [created: entry.created, items: entry.items.collect { it.field }]
        }
        
        // Sort the createdAndItemsValues list by 'created' date in descending order
        def sortedCreatedAndItemsValues = createdAndItemsValues.sort { a, b -> b.created <=> a.created }
        
        // Get the most recent 'created' value and its corresponding 'items' value
        def mostRecentEntry = sortedCreatedAndItemsValues.first()
        
        // Now mostRecentEntry contains the most recent 'created' value and its corresponding 'items' value
        logger.warn("Most recent 'created' value: ${mostRecentEntry.created}")
        logger.warn("Corresponding 'items' value: ${mostRecentEntry.items}")
        
        if (mostRecentEntry.items.contains("Sprint")) {
            
            def result = get('/rest/api/2/issue/' + issueKey)
                .header('Content-Type', 'application/json')
                .asObject(Map)
                if (result.status == 200){
                    def subtaskType = result.body.fields.issuetype.subtask.toString() // Convert boolean to string
                    def customFieldStates = result.body.fields.customfield_10020.state.collect { it.toString() } // Convert all states to strings
                    logger.warn(subtaskType)
                    logger.warn(customFieldStates)
                    if(subtaskType == 'false' && customFieldStates.contains('active')){
                        
                        def resp = post("/rest/api/2/issue/${issueKey}/notify")
                         .header("Content-Type", "application/json")
                         .body([
                             "subject": "Issue " + issueKey + " has been Sprint updated",
                             "htmlBody": "Summary: ${result.body.fields.summary}",
                             "to": [
                                 "users": [
                                     [
                                         "emailAddress": "charanv@devtools.in"
                                     ]
                                 ]
                             ]
                         ])
                         .asString()
                    }
                    } else {
                        return "Failed to find issue: Status: ${result.status} ${result.body}"
                    }
        
        } else {
            logger.warn("not sprint")
        }

15. **Edit fields upon moving to Not started**

        def issueKey = issue.key
        
        // Fetch the issue details
        def result = get('/rest/api/2/issue/' + issueKey)
            .header('Content-Type', 'application/json')
            .asObject(Map)
        
        if(result.body.fields.issuetype.name == 'Sub-task')
        {
        // Get the value of the source custom field
        def options = result.body.fields.customfield_10059.value
        def duedate = result.body.fields.customfield_10058
        
        // Ensure options is a list
        if (options instanceof List && options.size() > 0) {
            // Create a list to store the new values for customfield_10061
            def newValues = options.collect { option -> ["value": option.toString()] }
            
            // Perform the update to copy all options to customfield_10061
            def result2 = put('/rest/api/2/issue/' + issueKey)
                .header('Content-Type', 'application/json')
                .body([
                    fields: [
                        "customfield_10061": newValues,
                        "customfield_10060" : duedate
                    ]
                ])
                .asString()
            
            // Print the response body for the update
            println("Update result: ${result2.body}")
        } else {
            println("No options found in customfield_10059")
        }
        }

16. **Move Epic to in progres when child started**

        def issueKey = issue.key

        // Get the changelog for the issue
        def changelogResponse = get('/rest/api/3/issue/' + issueKey + '/changelog?orderBy=-created')
                                .header('Content-Type', 'application/json')
                                .asObject(Map)
        
        // Check if the request was successful
        if (changelogResponse.status != 200) {
           logger.error("Failed to fetch changelog for issue $issueKey. Status code: ${changelogResponse.status}")
           return;
        }
        
        // Extract the changelog entries
        def changelog = changelogResponse.body.values
        
        // Iterate through changelog entries and extract 'created' and 'items' values
        def createdAndItemsValues = changelog.collect { entry ->
            [created: entry.created, items: entry.items.collect { it.field }]
        }
        
        // Sort the createdAndItemsValues list by 'created' date in descending order
        def sortedCreatedAndItemsValues = createdAndItemsValues.sort { a, b -> b.created <=> a.created }
        
        // Get the most recent 'created' value and its corresponding 'items' value
        def mostRecentEntry = sortedCreatedAndItemsValues.first()
        
        // Now mostRecentEntry contains the most recent 'created' value and its corresponding 'items' value
        logger.warn("Most recent 'created' value: ${mostRecentEntry.created}")
        logger.warn("Corresponding 'items' value: ${mostRecentEntry.items}")
        
        if (mostRecentEntry.items.contains("status")) {
            
                        def result = get('/rest/api/2/issue/' + issueKey)
                            .header('Content-Type', 'application/json')
                            .asObject(Map)
                            if (result.status == 200){
                                def transitionId = 21
                                def issueResult = get("/rest/api/2/issue/${issueKey}")
                            .header('Content-Type', 'application/json')
                            .asObject(Map)
        
                    if (issueResult.status != 200) {
                        logger.warn("Failed to find issue: Status: ${issueResult.status} ${issueResult.body}")
                    }
        
                    def parentKey = issueResult.body.fields?.parent?.key
        
                    if (parentKey) {
        
                    if(issueResult.body.fields?.parent?.fields.issuetype.name == 'Epic' && issueResult.body.fields?.parent?.fields.status.name != "In Progress"){
                    // Retrieve all child issues
                    def childIssuesResult = get("/rest/api/2/search")
                            .queryString("jql", "parent=${parentKey}")
                            .asObject(Map)
        
                    assert childIssuesResult.status >= 200 && childIssuesResult.status <= 300
        
                    def childIssues = childIssuesResult.body.issues as List<Map>
        
                    // Check if at least one child issue is "In Progress"
                    def anyInProgress = childIssues.any { child ->
                        def childResult = get("/rest/api/2/issue/${child.key}")
                                .header('Content-Type', 'application/json')
                                .asObject(Map)
        
                        if (childResult.status == 200) {
                            return childResult.body.fields.status.name == "In Progress"
                        } else {
                            return false
                        }
                    }
        
                    if (anyInProgress) {
                        // Transition the parent issue
                        def transition = post("/rest/api/2/issue/${parentKey}/transitions")
                                .header("Content-Type", "application/json")
                                .body([transition: [id: transitionId]])
                                .asObject(Map)
                    } else {
                        logger.warn("No child issues are in progress.")
                    }
                    }
                    else{
        
                        logger.warn("It is not a Standard issue")
                    } 
                            }
                            else{
                                logger.warn("Parent issue not found for ${issueKey}")
                            }
                            }
                    
        } else {
            logger.warn("not sprint")
        }


17. **Send email for ticket creation Viction (Filter Summary )**
   
            // Set the Jira issue key
            def issueKey = issue.key
            
            // Fetch the issue details from the Jira REST API
            def result = get('/rest/api/2/issue/' + issueKey)
                    .header('Content-Type', 'application/json')
                    .asObject(Map)
            
            // Ensure the request was successful
            if (result.status == 200) {
                def issueDetails = result.body
                def summary = issueDetails.fields.summary
                def subtaskType = issueDetails.fields.issuetype.subtask
                def issueType = issueDetails.fields.issuetype.name
                def reporterId = issueDetails.fields.reporter?.accountId
                def customNumber = issueDetails.fields?.customfield_10083
                def customRuleName = issueDetails.fields?.customfield_10084
            
                // Find the first comma in the summary
                def commaIndex = summary.indexOf(',')
            
                if (commaIndex != -1) {
                    // Get the part after the first comma, trimming leading and trailing whitespace
                    def summaryAfterComma = summary.substring(commaIndex + 1).trim()
            
                    // Extract relevant fields from the issue details
                    
            
            
                  
                    logger.warn("Subtask type: ${subtaskType}, Issue type: ${issueType}, Reporter ID: ${reporterId}, Custom number: ${customNumber}, Custom rule name: ${customRuleName}")
            
                    // Check the conditions for sending the notification
                    if ((issueType == "Story" || issueType == "Task") &&
                    (!subtaskType) &&
                    (reporterId == '630a0d15ec02b5f28b63a024') &&
                    ((customNumber == 5) || (customNumber == 7)) &&
                    (customRuleName.contains("LVRP"))) {
                            
                        // Send the notification to a specific email address
                        def notifyResponse = post("/rest/api/2/issue/${issueKey}/notify")
                            .header("Content-Type", "application/json")
                            .body([
                                "subject": summaryAfterComma + " Blocked Faster Payment Victim",
                                "htmlBody": issueDetails.fields.description,
                                "to": [
                                    "users": [
                                        ["emailAddress": "charanv@devtools.in"]
                                    ]
                                ]
                            ])
                            .asString()
                        
                         logger.warn(notifyResponse)
                    } else {
                        logger.warn("Conditions for sending the notification were not met")
                    }
                } else {
                    // No comma in the summary
                    logger.warn("Summary does not contain a comma")
                }
            } else {
                // Log error details for failed requests
               logger.warn("Failed to fetch issue details: Status ${result.status} - ${result.body}")
            }

 18. **Story points updates(comment addig if story pount is empty)**


            import java.util.regex.*
            
            // Step 1: Get the issue information
            def issueKey = 'SR-65'
            
            def issueResult = get('/rest/api/2/issue/' + issueKey)
                .header('Content-Type', 'application/json')
                .asObject(Map)
            
            def reporter = issueResult.body.fields.reporter?.accountId
            def assignee = issueResult.body.fields.assignee?.accountId
            
            def commentText = """
            Hi [~accountid:${reporter}] [~accountid:${assignee}],
            
            Please update story points estimate as this story is already DoR ready.
            """
            
            
            def text = "Please update story points estimate as this story is already DoR ready."
            
            // Step 2: Get existing comments for the issue
            def commentsResult = get('/rest/api/2/issue/' + issueKey + '/comment')
                .header('Content-Type', 'application/json')
                .asObject(Map)
            
            // Step 3: Check for duplicate comments
            def comments = commentsResult.body.comments
            def commentAlreadyExists = comments.any { comment ->
                comment.body.contains(text.trim())
            }
            
            
            
            if(issueResult.body.fields.customfield_10035 == null){
            if (!commentAlreadyExists) {
                // Step 4: Add the new comment only if it doesn't already exist
                def addCommentResult = post('/rest/api/2/issue/' + issueKey + '/comment')
                    .header('Content-Type', 'application/json')
                    .body(["body": commentText.trim()])
                    .asObject(Map)
            
                println(addCommentResult) // This should output the response from Jira, you can check if it was successful
            } else {
                println("Duplicate comment found, not adding a new one.")
            }
            }else{
                println("Story points not null")
            }

19. Send web request

            import groovy.json.JsonOutput
            import org.apache.http.HttpEntity
            import org.apache.http.client.methods.HttpPost
            import org.apache.http.entity.StringEntity
            import org.apache.http.impl.client.HttpClients
            
            // Convert objects to JSON strings
            def issueString = JsonOutput.toJson(issue)
            def userString = JsonOutput.toJson(user)
            
            // Define the timestamp
            def timestamp1 = JsonOutput.toJson(timestamp)
            
            // Create a map with the desired format
            def combinedJson = [
                issue: issueString,
                user: userString,
                timestamp: timestamp1
            ]
            
            // Convert the combined map to a JSON string
            def combinedJsonString = JsonOutput.toJson(combinedJson)
            
            // Define the endpoint URL
            def endpointUrl = "https://smee.io/3rWqEkwTZ9EyFeo2"
            
            // Create an HttpClient instance
            def httpClient = HttpClients.createDefault()
            
            // Create a POST request
            def postRequest = new HttpPost(endpointUrl)
            
            // Set the content type of the request
            postRequest.setHeader("Content-Type", "application/json")
            
            // Set the JSON payload for the request
            postRequest.setEntity(new StringEntity(combinedJsonString))
            
            // Execute the request and get the response
            def response = httpClient.execute(postRequest)
            
            // Log the response if needed
            logger.warn(response.toString())
            
            // Close the HttpClient
            httpClient.close()

