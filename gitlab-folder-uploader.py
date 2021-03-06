import requests
import sys
import json
import os
import pathlib
import git
import shutil

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
    print(path_to_upload)
    upload_directory = os.path.abspath(path_to_upload)
    upload_files = os.listdir(upload_directory)

    for filename in upload_files:
        filepath = os.path.join(upload_directory, filename)
        if os.path.isdir(filepath):
            if not filename.startswith("."):
                if os.path.exists(os.path.join(filepath,".git")):
                    print("\ncreate project",filename)
                    add_project(filepath, filename, parent_id)
                else :
                    #web_path += "/" +filename
                    print("\ncreate group", filename)
                    id = get_id_from_json(add_group(filename, filename, parent_id))
                    my_walk(filepath, id)
            


def change_origin(folder_path, origin_url):
    origin_url_with_key = origin_url.replace("https://","https://oauth2:"+ private_token+"@")
    #origin_url_with_key += ".git"
    try:
        repo = git.Repo(folder_path)

        try:
            origin = repo.remotes.origin
        except AttributeError:
            repo.create_remote('origin', origin_url_with_key)

        origin = repo.remotes.origin
        with origin.config_writer as cw:
            cw.set("pushurl", origin_url_with_key)
            cw.set("url", origin_url_with_key)
            cw.release()
        try:
            origin.push('master')
        except git.exc.GitCommandError as err:
            print(err)

        
    except git.exc.InvalidGitRepositoryError:
        
        previous_dir = os.getcwd()

        os.chdir(folder_path)

        shutil.rmtree(".git", ignore_errors=True)

        repo = git.Repo.init(".")
 
        repo.create_remote('origin', origin_url_with_key)
        
        repo.git.add(".","--all")
        try:
            repo.git.commit('-m',"initial commit")
            repo.remotes.origin.push('master')
        except git.exc.GitCommandError as err:
            print(err)

        
        
        os.chdir(previous_dir)

        




def add_project(folder_path, project_name, namespace_id):
    global gitlab_api_url
    global private_token
    
    payload = {"name":project_name, "visibility":"internal","namespace_id":namespace_id}
    
    
    url = gitlab_api_url + "/projects"
    
    response = requests.post(url, data=payload, headers=headers, verify=False)
    print(response.status_code, response.reason,"\n")
    #print(response.text)
        
    parsed_json = json.loads(response.text)
    change_origin(folder_path, parsed_json["http_url_to_repo"] + "/")


def add_group(group_name, group_path, parent_id=None):
    global gitlab_api_url
    global private_token
    
    group_path = group_path.replace('\\','/')
    payload = {"name":group_name, "path":group_path, "visibility":"internal"}
    if parent_id != None:
        payload["parent_id"] = parent_id
    
    
    url = gitlab_api_url + "/groups"
    
    response = requests.post(url, data=payload, headers=headers, verify=False)
    
    print(response.status_code, response.reason,"\n")
    
    return response.text
    
def execute():
    cwd = os.getcwd()
    path, folder = os.path.split(cwd)
    print("create group", folder)
    id = get_id_from_json(add_group(folder,folder))
    my_walk(cwd, id)
       
      

 
    

execute()
