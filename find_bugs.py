# -*- coding: utf-8 -*-

"""
Identify bugfixes in ml tool repository
@author: Zerui Mu
"""

import json
import re


def find_bug(dic_issues, dic_log, pattern):
    i = 0 # Used to display progress
    no_matches = []
    matches_per_issue = {}
    issue_list = {}
    total_matches = 0
    
    """make issue lists"""
    for issue in dic_issues:
        issue_list[issue['number']] = {}

        created_date = issue['created_at'].replace('T', ' ').replace('Z', '') + " +0000"
        issue_list[issue['number']]['creationdate'] = created_date

        closed_date = issue['closed_at'].replace('T', ' ').replace('Z', '') + " +0000"
        issue_list[issue['number']]['resolutiondate'] = closed_date
        
    for issue in issue_list:
        nbr = issue
        matches = []
        for commit in dic_log:
            pat = pattern.format(nbr=nbr)
            if re.search(pat, commit):
                if commit_filter(commit):                   
                    matches.append(commit)
        total_matches += len(matches)
        matches_per_issue[issue] = len(matches)
        
        if matches:
            selected_commit = commit_selector_heuristic(matches)
            if not selected_commit:
                no_matches.append(issue)
            else:
                issue_list[issue]['hash'] = (\
                    re.search('commit [a-z0-9]+', \
                    selected_commit).group(0)).replace('commit ', '')
                issue_list[issue]['commitdate'] = (\
                    re.search('Date:   [a-zA-Z0-9\D]{23,27}[+-](\d){4,4}',\
                    selected_commit).group(0)).replace('Date:   ', '')
        else:
            no_matches.append(issue)
        
        # Progress counter
        i += 1
        if i % 10 == 0:
            print(i, end='\t')
        if i % 100 == 0:
            print('\r')

    print('Total issues: ' + str(len(issue_list)))
    print('Issues matched to a bugfix: ' + str(len(issue_list) - len(no_matches)))
    print('Percent of issues matched to a bugfix: ' + \
          str((len(issue_list) - len(no_matches)) / len(issue_list)))
    for key in no_matches:
        issue_list.pop(key)

    return issue_list, matches_per_issue


def commit_filter(commit):
    """ Pick out bug-fixing commit.
    If the commit only have one line, check whether it has a key word (FIX|BUG).
    If not, check every update in this commit.
    """
    pat_fix = "[Ff][Ii][Xx]|[Bb][Uu][Gg]"
    pat_other_files = "DOC|TST|EXA|\.rst" # documentation | test | example | .rst
    
    if not re.search("\*", commit):
        if re.search(pat_fix, commit) and not re.search(pat_other_files, commit):
            return True
    else:
        commit = commit.split("*")
        for update in commit:
            if re.search(pat_fix, update) and not re.search(pat_other_files, update):
                return True
    return False     
    
    
def commit_selector_heuristic(commits):
    """ Helper method for find_bug_fixes.
    Commits are assumed to be ordered in reverse chronological order.
    Given said order, pick first commit that does not match the pattern.
    If all commits match, return newest one. """
    for commit in commits:
        if not re.search('MRG', commit): # merge
            return commit
    return commits[0]

    
if __name__ == '__main__':
    mltool_name = 'sklearn'
    
    """ open files by ml tool name """
    f_issues = open('./' + mltool_name + '/' + mltool_name + '_all_issues.json', 'r', encoding='utf-8')
    con_issues = f_issues.read().replace('\n', '').replace('\r', '')
    dic_issues = json.loads(con_issues, strict=False)
    
    f_log = open('./' + mltool_name + '/' + mltool_name + '_commit.log', 'r', encoding='utf-8')
    con_log = f_log.read().replace('\n', '').replace('\r', '')
    dic_log = json.loads(con_log, strict=False)
    
    pattern = '\(#{nbr}\)'
    issue_list, matches_per_issue = find_bug(dic_issues, dic_log, pattern)
    
    """ save bug fix issue list """
    with open('./' + mltool_name + '/' + mltool_name + '_bug_fix_list.json', 'w') as f:
        f.write(json.dumps(issue_list))
