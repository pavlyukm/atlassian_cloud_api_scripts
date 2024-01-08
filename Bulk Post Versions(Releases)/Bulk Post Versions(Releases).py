"""
Useful when need to copy releases from another project. Export json with releases:https://developer.atlassian.com/cloud/jira/platform/rest/v3/api-group-project-versions/#api-rest-api-3-project-projectidorkey-version-get
Edit project ID and delete shit like userStartDate and userEndDate because it errors out. Can use following code for ediditing:
with open("file.json", "r") as file:
    data_list = json.load(file)

# Iterate through each instance and remove the "userReleaseDate" parameter
for instance in data_list:
    if "userStartDate" in instance:
        del instance["userStartDate"]

# Save the modified data back to a file or use it as needed
with open("CSA_versions.json", "w") as file:
    json.dump(data_list, file, indent=4)
"""
import requests
from requests.auth import HTTPBasicAuth
import json


with open("versions.json", "r") as file:
    data_list = json.load(file)

url = "https://SITE.atlassian.net/rest/api/3/version"

auth = HTTPBasicAuth("USERNAME", "UAT")

headers = {
  "Accept": "application/json",
  "Content-Type": "application/json"
}
'''
Example version in dump:
payload = json.dumps( {
  "archived": 'false',
  "description": "description.",
  "name": "name",
  "projectId": 10714,
  "startDate": "2022-09-15",
  "releaseDate": "2023-10-05",
  "released": 'true'
} )
'''
for data in data_list:
    response = requests.request(
       "POST",
       url,
       json=data,
       headers=headers,
       auth=auth
    )

    print(json.dumps(json.loads(response.text), sort_keys=True, indent=4, separators=(",", ": ")))
