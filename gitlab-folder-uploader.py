import requests
import sys
import json
import os
import pathlib
private_token = sys.argv[1]

headers = {
        'PRIVATE-TOKEN': private_token
}

gitlab_url = sys.argv[2]



gitlab_api_url = gitlab_url + "/api/v4"

def get_id_from_json(json_input):
    parsed_json = json.loads(json_input)
    return parsed_json['id']

def my_walk(path_to_upload, parent_id):
    
    upload_directory = os.path.abspath(path_to_upload)
    upload_files = os.listdir(upload_directory)

    for filename in upload_files:
        filepath = os.path.join(upload_directory, filename)
        if os.path.isdir(filepath):
            if not filename.startswith("."):
                if os.path.exists(os.path.join(filepath,".git")):
                    print("create project",filename)
                    add_project(filename, parent_id)
                else :
                    #web_path += "/" +filename
                    print("create group", filename)
                    id = get_id_from_json(add_group(filename, filename, parent_id))
                    my_walk(filepath, id)
            
    

def add_project(project_name, namespace_id):
    global gitlab_api_url
    global private_token
    
    payload = {"name":project_name, "visibility":"internal","namespace_id":namespace_id}
    
    
    url = gitlab_api_url + "/projects"
    
    response = requests.post(url, data=payload, headers=headers, verify=False)
    print(response.status_code, response.reason)
    
    
    return response.text




def add_group(group_name, group_path, parent_id=None):
    global gitlab_api_url
    global private_token
    
    group_path = group_path.replace('\\','/')
    payload = {"name":group_name, "path":group_path, "visibility":"internal"}
    if parent_id != None:
        payload["parent_id"] = parent_id
    
    
    url = gitlab_api_url + "/groups"
    
    response = requests.post(url, data=payload, headers=headers, verify=False)
    
    
    
    return response.text
    
def execute():
    cwd = os.getcwd()
    path, folder = os.path.split(cwd)
    print("create group", folder)
    id = get_id_from_json(add_group(folder,folder))
    my_walk(cwd, id)
       
      

 
    

execute()