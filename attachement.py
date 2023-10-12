import requests
import csv
import re

# Set your GitLab project ID and access token
PROJECT_ID = 41299063
ACCESS_TOKEN = "glpat-XsRzi9SD8yHJyMavhhh3"

# Define the API endpoint URL
BASE_URL = f"https://gitlab.com/api/v4/projects/{PROJECT_ID}"

# Function to get issue IDs
def get_issue_ids():
    issues_url = f"{BASE_URL}/issues?per_page=1"  # Increase per_page as needed
    issue_ids = []
    
    page = 1
    while True:
        response = requests.get(issues_url + f"&page={page}", headers={"PRIVATE-TOKEN": ACCESS_TOKEN})
        
        if response.status_code == 200:
            issues_data = response.json()
            if not issues_data:
                break  # No more issues to retrieve
            issue_ids.extend([issue["iid"] for issue in issues_data])
            page += 1
        else:
            print(f"Failed to retrieve issue IDs. Status code: {response.status_code}")
            break
    
    return issue_ids

# Function to retrieve notes for a specific issue
def get_notes_for_issue(issue_id):
    notes_url = f"{BASE_URL}/issues/{issue_id}/notes"
    response = requests.get(notes_url, headers={"PRIVATE-TOKEN": ACCESS_TOKEN})
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Failed to retrieve notes for issue {issue_id}. Status code: {response.status_code}")
        return []

# Get issue IDs
issue_ids = get_issue_ids()

# Create a CSV file and write the data
with open("gitlab_data.csv", mode="w", newline="", encoding="utf-8") as csv_file:
    fieldnames = ["Issue ID", "Upload Paths"]
    writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
    writer.writeheader()

    for issue_id in issue_ids:
        upload_paths = []  # List to store upload paths for each issue
        notes = get_notes_for_issue(issue_id)
        for note in notes:
            # Check if "body" contains "/uploads/"
            body = note["body"]
            uploads = re.findall(r'/uploads/[^)]*', body)
            if uploads:
                upload_paths.extend(uploads)

        # Write the issue ID and upload paths to the CSV file
        writer.writerow({
            "Issue ID": issue_id,
            "Upload Paths": ", ".join(upload_paths)  # Comma-separated list of paths
        })

print("Data has been saved to gitlab_data.csv")
