import requests
import csv

# Set your GitLab project ID and access token
PROJECT_ID = 41299063
ACCESS_TOKEN = "glpat-XsRzi9SD8yHJyMavhhh3"

# Define the API endpoint URLs
BASE_URL = f"https://gitlab.com/api/v4/projects/{PROJECT_ID}"
ISSUES_URL = f"{BASE_URL}/issues"
LINKS_URL = f"{BASE_URL}/issues/{{issue_id}}/links"

# Function to get all issues in the project
def get_all_issues():
    all_issues = []
    page = 1
    while True:
        issues_url = f"{ISSUES_URL}?per_page=100&page={page}"
        response = requests.get(issues_url, headers={"PRIVATE-TOKEN": ACCESS_TOKEN})
        
        if response.status_code == 200:
            issues_data = response.json()
            if not issues_data:
                break  # No more issues to retrieve
            all_issues.extend(issues_data)
            page += 1
        else:
            print(f"Failed to retrieve issues. Status code: {response.status_code}")
            break
    
    return all_issues

# Function to retrieve linked issues for a specific issue
def get_linked_issues(issue_id):
    links_url = LINKS_URL.replace("{issue_id}", str(issue_id))
    response = requests.get(links_url, headers={"PRIVATE-TOKEN": ACCESS_TOKEN})
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Failed to retrieve linked issues for issue {issue_id}. Status code: {response.status_code}")
        return []

# Get all issues in the project
all_issues = get_all_issues()

# Create a CSV file and write the data
with open("gitlab_data.csv", mode="w", newline="", encoding="utf-8") as csv_file:
    fieldnames = [
        "project_id", "issue_id","issue_title", "linked_issue_id", "linked_issue_title"
    ]
    writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
    writer.writeheader()

    for issue in all_issues:
        issue_id = issue["iid"]
        linked_issues = get_linked_issues(issue_id)
        for linked_issue in linked_issues:
            writer.writerow({
                "project_id": PROJECT_ID,
                "issue_id": issue_id,
                "issue_titile":issue["title"],
                "linked_issue_id": linked_issue["iid"],
                "linked_issue_title": linked_issue["title"]
            })

print("Data has been saved to gitlab_data.csv")
