"""
Useful when need to bulk add users to internal user groups. Need to have excel: 
user ID - Group Name
"""
import requests
import openpyxl


base_url = "https://your-jira-instance.atlassian.net"
api_token = "your-api-token"
api_email = "your-email"


api_endpoint = f"{base_url}/rest/api/3/group/user"


def add_user_to_group(group_name, user_id):
    headers = {
        "Authorization": f"Basic {api_email}:{api_token}"
    }
    data = {
        "groupname": group_name,
        "name": user_id
    }

    response = requests.post(api_endpoint, headers=headers, json=data)
    if response.status_code == 201:
        print(f"Added user {user_id} to group {group_name}")
    else:
        print(f"Failed to add user {user_id} to group {group_name}. Status code: {response.status_code}")


workbook = openpyxl.load_workbook('user_groups.xlsx')
sheet = workbook.active

for row in sheet.iter_rows(min_row=2, values_only=True):  # Assuming headers are in the first row
    user_id, group_name = row
    add_user_to_group(group_name, user_id)

workbook.save('user_groups_updated.xlsx')
