#!/usr/bin/env python

# This script lets you initalize a new repo on github
# from the command line
# All you need is a github user and a password
# 11. sep 2013 @ Svenardo
# License: CC0 1.0 Universal (CC0 1.0)

import os
import subprocess
import getpass
import json
import sys

# Set current dir
p = subprocess.Popen(["pwd"], stdout=subprocess.PIPE)
out, err = p.communicate()
working_dir=(out.decode('utf8')).strip()

passw=getpass.unix_getpass(prompt='Password: ', stream=None)

p = subprocess.Popen(["git","config","github.user"], stdout=subprocess.PIPE)
out, err = p.communicate()
user=(out.decode('utf8')).strip()

# check if ok
curl_creds="curl -su '"+user+":"+passw+"' https://api.github.com/user/repos "
check_creds = subprocess.check_output(curl_creds,shell=True)

# Error check
json_data=json.loads(check_creds.decode("utf-8"))

stop_run=False

try:
    if "Bad credentials" in json_data["message"]:
        print(json_data["message"])
        stop_run=True
    if "Maximum number" in json_data["message"]:
        print(json_data["message"])
        stop_run=True
    if "Validation Failed" in json_data["message"]:
        print(json_data["message"])
        stop_run=True
except:
    print("Password OK")

if(stop_run):
    sys.exit(0)
    
# Initialize repo
strInit="git init"
process = subprocess.Popen(strInit, stdout=subprocess.PIPE, stderr=None, shell=True)
output = process.communicate()

repo=input("Name of new repo: ");
desc=input("Description: ");

# Create repo:
curl_cmd="curl -su '"+user+":"+passw+"' https://api.github.com/user/repos -d '{\"name\":\""+repo+"\", \"description\":\""+desc+"\", \"private\": false, \"has_issues\": true, \"has_downloads\": true, \"has_wiki\": false}'"
create_repo= subprocess.Popen(curl_cmd, stdout=subprocess.PIPE, stderr=None, shell=True)
create_repo_output = create_repo.communicate()
json_data=json.loads(create_repo_output[0].decode("utf-8"))

# check messages
try:
    if "Validation Failed" in json_data["message"]:
        stop_run=True
        print(json_data["message"])
        print("You may already have a repo with this name")
except:
    print("")
    
if(stop_run):
    sys.exit(0)

full_name=json_data["full_name"]

# Set origin
add_origin="git remote add origin git@github.com:"+full_name+".git";
process = subprocess.Popen(add_origin, stdout=subprocess.PIPE, stderr=None, shell=True)
output = process.communicate()

print("Git repo initialized as "+full_name);
print("Add files and commit at will :). Remember to use 'push -u origin master' for your first commit");
