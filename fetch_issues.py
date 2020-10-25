# -*- coding: utf-8 -*-
"""
@author: Zerui Mu
"""

import requests
import json

def getHTML(url):
    try:
        headers = {
            "Authorization": "token [YOUR_TOKEN]"}
        r = requests.get(url, headers = headers)
        r.raise_for_status
        r.encoding = r.apparent_encoding
        return r.text
    except:
        return "Wrong!"
    

def getAllIssues(url, total_issue):
    last_page = int(total_issue / 100 + 1)
    dic_issues = []
    all_pages = []
    missed_pages = []
    
    for i in range(last_page):
        all_pages.append(str(i+1))
        missed_pages.append(str(i+1))
    
    while len(missed_pages) != 0:
        for i in missed_pages:
            url_request = url + '&page=' + i
            content = getHTML(url_request).replace('\n', '').replace('\r', '')
            if content == "Wrong!":
                print("Page " + i + " missed!")
            else:
                dic_request = json.loads(content)
                dic_issues = dic_issues + dic_request
                all_pages.remove(i)
                print("Page " + i + " added!")
        missed_pages = all_pages[:]
        print("\nAnother round!\n")
            
    dic_issues.sort(key=lambda x:x['number'])
    return dic_issues, missed_pages


if __name__ == "__main__":
    urlSK = "https://api.github.com/repos/scikit-learn/scikit-learn/issues?per_page=100&state=closed"
    urlTF = "https://api.github.com/repos/tensorflow/tensorflow/issues?per_page=100&state=closed"
    total_issue = 18620
    issues, missed = getAllIssues(urlSK, total_issue)
    