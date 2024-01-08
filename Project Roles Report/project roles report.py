"""
This parses every project in Jira Cloud site and checks EVERY project role since they are global and only prints actors if it is not empty in following format:
Project: <Key>, Role: <Role name>, Users: {actors: [list of users]}
"""
import requests
import base64


def get_jira_projects(api_url, auth_header):
    url = f"{api_url}/project/search"
    projects = []

    while url:
        response = requests.get(url, headers=auth_header)
        response.raise_for_status()
        data = response.json()
        projects.extend(data.get('values', []))
        url = data.get('nextPage', None)

    return projects


def get_project_roles(api_url, auth_header, project_key):
    url = f"{api_url}/project/{project_key}/role"
    response = requests.get(url, headers=auth_header)
    response.raise_for_status()

    try:
        roles_data = response.json()

        if isinstance(roles_data, dict):
            # Handle the case where roles are returned as a dictionary
            return {role_id.split('/')[-1]: role_name for role_name, role_id in roles_data.items()}
        elif isinstance(roles_data, list):
            # Handle the case where roles are returned as a list
            roles_dict = {}
            for role in roles_data:
                if isinstance(role, dict):
                    roles_dict[role['id']] = role['name']
                elif isinstance(role, str) and role.startswith(api_url):
                    role_id = role.split('/')[-1]
                    roles_dict[role_id] = role_id  # Using ID as the name if the name is not available
            return roles_dict
        else:
            return {}
    except ValueError:
        return {}


def get_role_users(api_url, auth_header, project_key, role_id):
    url = f"{api_url}/project/{project_key}/role/{role_id}"
    response = requests.get(url, headers=auth_header)

    try:
        response.raise_for_status()
        data = response.json()

        # Extract display names from actors
        actors = data.get('actors', [])
        display_names = [actor.get('displayName', '') for actor in actors]

        return {'actors': display_names}

    except requests.exceptions.HTTPError as err:
        if response.status_code == 404:
            print(f"Role Users: 404 - Role not found for {project_key} / {role_id}")
            return {'actors': []}
        else:
            raise err

def generate_report(projects, auth_header, api_url, excluded_roles=None):
    report = {}
    excluded_roles = excluded_roles or set()

    for project in projects:
        project_key = project['key']
        project_roles = get_project_roles(api_url, auth_header, project_key)

        for role_id, role_name in project_roles.items():
            if role_name not in excluded_roles:
                role_users = get_role_users(api_url, auth_header, project_key, role_id)
                if role_users['actors']:
                    print(f"Project: {project_key}, Role: {role_name}, Users: {role_users}")

                report.setdefault(project_key, {}).setdefault(role_name, []).extend(role_users['actors'])

    return report


def main():
    #replace with your actual Jira instance URL, username, and API token
    jira_api_url = "https://INSTANCE.atlassian.net/rest/api/2"
    jira_username = "EMAIL"
    jira_api_token = "PAT"
    credentials = f"{jira_username}:{jira_api_token}"
    auth_header = {"Authorization": "Basic " + base64.b64encode(credentials.encode('utf-8')).decode('utf-8')}

    #exclude this because otherwise it throws error
    excluded_roles = {'atlassian-addons-project-access'}

    projects = get_jira_projects(jira_api_url, auth_header)
    report = generate_report(projects, auth_header, jira_api_url, excluded_roles)

    #this can run VERY long depending on amount of projects so it's nice to have a print and save
    print(report)
    with open('jira_report.json', 'w') as json_file:
        json.dump(report, json_file)

main()
