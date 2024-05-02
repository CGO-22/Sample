1. **Set Organizations Using reporter's email domain**


        def issueKey = issue.key
        
        
        // Attempt to update the custom field with the organization data
        def updateResult = put("/rest/api/2/issue/" + issueKey)
            .header("Content-Type", "application/json")
            .body([
                fields: [
        
                    customfield_10002 : [1]
                ]
            ])
            .asObject(Map)
        
        // Check if the update was successful
        if (updateResult.status >= 200 && updateResult.status < 300) {
            logger.info("Successfully updated the issue with one organization.")
        } else {
            logger.warn("Failed to update the issue: Status: ${updateResult.status}, Body: ${updateResult.body}")
        }
