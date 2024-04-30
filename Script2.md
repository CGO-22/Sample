1. **Assign cuurent sprint value for failed DBT jobs (mem and mam)**

    def issueKey = issue.key
    def issueResult = get('/rest/api/2/issue/' + issueKey)
        .header('Content-Type', 'application/json')
        .asObject(Map)

    if(issueResult.body.fields.project.key == "SR" && (issueResult.body.fields.summary.contains("tide-mam") || issueResult.body.fields.summary.contains("tide-mem") ) ){
    
        def sprintId = 13 // Example: update with correct Sprint ID
    
        def result2 = put('/rest/api/2/issue/' + issueKey)
            .header('Content-Type', 'application/json')
            .body([
                fields: [
                    customfield_10020: sprintId // Sprint ID should be a number
                ]
            ])
            .asString()
    }

2. 
