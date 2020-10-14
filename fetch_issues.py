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
    

def getAllIssues(url):
    issues_number = 18620
    last_page = int(issues_number / 100 + 1)
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
            
    return dic_issues, missed_pages


if __name__ == "__main__":
#    urlIssues = "https://api.github.com/repos/scikit-learn/scikit-learn/issues?per_page=100&state=closed&labels=bug"
    urlIssues = "https://api.github.com/repos/scikit-learn/scikit-learn/issues?per_page=100&state=closed"
    issues, missed = getAllIssues(urlIssues)