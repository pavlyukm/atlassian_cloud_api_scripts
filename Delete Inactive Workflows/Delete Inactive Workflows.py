import requests
import json
import os


base_url = "https://URL.atlassian.net/rest/api/3/workflow/"
username = os.environ['username']
password = os.environ['password']

#You must export inactive workflows as a json first https://developer.atlassian.com/cloud/jira/platform/rest/v3/api-group-workflows/#api-rest-api-3-workflow-search-get (filter out canDelete: True
#Note to self add this functionality to this script
with open('inactiveworkflow.json', 'r') as jsonfile:
    data = json.load(jsonfile)

    session = requests.Session()
    session.auth = (username, password)

    # Iterate over the JSON data and send DELETE requests for each entityId
    for item in data:
        entityId = item.get("id", {}).get("entityId")

        if entityId:
            api_url = f"{base_url}{entityId}"

            response = session.delete(api_url)

            if response.status_code == 204:
                print(f"Deleted entityId {entityId}")
            else:
                print(f"Failed to delete entityId {entityId} with status code {response.status_code}")
