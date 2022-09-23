# Copyright (c) 2009 IW.
# All rights reserved.
#
# Author: liuqw <qingwei.liu@foxmail.com>
# Date:   2022/9/23
"""Delete projects in harbor, such as personal-xxxxx, project-xxxx
harbor version: 1.7.1
"""

import base64

import requests

host = "harbor.ainnovation.com"
pro_url = "https://harbor.ainnovation.com/api/projects"
repo_url = "https://harbor.ainnovation.com/api/repositories"
name = "admin"
password = "123qwE123"

# header
# format name password params
format_str = "%s:%s" % (name, password)
format_str = format_str.encode()
encoded_str = base64.b64encode(format_str).decode()
# print(encoded_str)
headers = {
    "Host": host,
    "User-Agent": "PostmanRuntime/7.29.0",
    "Accept": "*/*",
    "Accept-Encoding": "gzip,deflate, br",
    "Connection": "keep-alive",
    "Authorization": "Basic %s" % encoded_str,
}

r = requests.get(pro_url, headers=headers)
if r.status_code != 200:
    print("Status code: %d" % r.status_code)
    print(r.text)
    # print(r.content)
    exit(1)

# delete project
projects = r.json()
cnt = 0
repoCnt = 0
for project in projects:
    pname = project["name"]
    pid = project["project_id"]
    if not pname.startswith("project-"):
        continue

    # delete repos in project
    print("Enumerating project: %s" % pname)
    found_repos = 100
    start_page = 1
    while found_repos == 100:
        params = {
            "project_id": pid,
            "page_size": 100,
            "page": start_page,
        }
        r = requests.get(repo_url, params=params, headers=headers)
        if r.status_code != 200:
            print("List project %s %d error at page %d, skip:" %
                  (pname, pid, start_page))
            break
        repos = r.json()
        for repo in repos:
            repo_name = repo["name"]
            # delete repo
            del_repo_url = "%s/%s" % (repo_url, repo["name"])
            del_repo_params = {"repo_name": repo["name"]}
            r = requests.delete(
                del_repo_url, headers=headers, params=del_repo_params)
            if r.status_code != 200:
                print("Delete repo %s failed, code %d, text %s.\n" %
                      (repo["name"], r.status_code, r.text))
                continue
            repoCnt += 1
            print("Delete repo successfully: %s." % repo["name"])

        found_repos = len(repos)
        start_page += 1

    # delete project
    del_pro_url = pro_url + "/" + str(pid)
    del_pro_params = {"project_id": pid}
    r = requests.delete(del_pro_url, headers=headers, params=del_pro_params)
    if r.status_code != 200:
        print("Delete project %d %s failed, code %d" %
              (pid, pname, r.status_code))
        continue
    cnt += 1

print("Deleted project: %d", cnt)
print("Deleted repos: %d", repoCnt)
