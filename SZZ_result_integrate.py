# -*- coding: utf-8 -*-
"""
Created on Fri Oct 23 16:02:44 2020

@author: Zerui Mu
"""

import os
import json


def open_json_files(mltool_name):
    file_path = os.getcwd() + '\\' + mltool_name + '\\SZZ_results\\'
    folders = os.listdir(file_path)
    dic_all_anno = {}
    
    for folder in folders:
        file = open(file_path + '\\' + folder + '\\results\\annotations.json', 'r', encoding = 'utf-8')
        content = file.read().replace('\n', '').replace('\r', '')
        dic = json.loads(content, strict = False)
        dic_all_anno.update(dic)
        
    return dic_all_anno


def sort_out_files_name(dic_anno):
    dic_files_name = {}
    for key in dic_anno:
        for change in dic_anno[key]:
            if change['filePath'] in dic_files_name:
                dic_files_name[change['filePath']] += 1
            else:
                dic_files_name[change['filePath']] = 1
    
    return dic_files_name

    
if __name__ == "__main__":
    mltool_name = 'sklearn'
    dic_anno = open_json_files(mltool_name)
    dic_files = sort_out_files_name(dic_anno)
    
    with open('./' + mltool_name + '/' + mltool_name + '_changed_files.json', 'w') as f:
        f.write(json.dumps(dic_files))
            
    