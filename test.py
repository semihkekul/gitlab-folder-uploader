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



path = os.path.join("android","not_git")

origin_url = gitlab_url +"/gitlab-folder-uploader/"+path

print(origin_url.find("https://"))


origin_url_with_key = origin_url.replace("https://","https://oauth2:"+ private_token+"@")
origin_url_with_key += ".git"

print(origin_url_with_key)

repo = git.Repo("./"+path)
try:
    origin = repo.remotes.origin
except AttributeError:
    repo.create_remote('origin', origin_url_with_key)
origin = repo.remotes.origin

with origin.config_writer as cw:
    cw.set("pushurl", origin_url_with_key)
    cw.set("url", origin_url_with_key)
    cw.release()
"""
origin.push()


print(os.path.join(path,".git"))

os.chdir(path)

shutil.rmtree(".git",ignore_errors=True)


repo = git.Repo.init(".")

repo.create_remote('origin', origin_url_with_key)


repo.git.add(".","--all")
repo.git.commit('-m',"initial commit")

repo.remotes.origin.push('master')
"""