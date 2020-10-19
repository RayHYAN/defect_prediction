# -*- coding: utf-8 -*-

from radon.raw import analyze
import json
import operator
import pandas as pd

def open_json_files(mltool_name):
    dic_radon = {}
    f_radon_raw = open('./radon_result/' + mltool_name + '/radon_' + mltool_name + '_raw.json', 'r', encoding='utf-8')
    con_radon_raw = f_radon_raw.read().replace('\n', '').replace('\r', '')
    dic_radon_raw = json.loads(con_radon_raw, strict=False)   
    
    f_radon_mi = open('./radon_result/' + mltool_name + '/radon_' + mltool_name + '_mi.json', 'r', encoding='utf-8')
    con_radon_mi = f_radon_mi.read().replace('\n', '').replace('\r', '')
    dic_radon_mi = json.loads(con_radon_mi, strict=False)
    
    f_radon_hal = open('./radon_result/' + mltool_name + '/radon_' + mltool_name + '_hal.json', 'r', encoding='utf-8')
    con_radon_hal = f_radon_hal.read().replace('\n', '').replace('\r', '')
    dic_radon_hal = json.loads(con_radon_hal, strict=False)
    
    f_radon_cc = open('./radon_result/' + mltool_name + '/radon_' + mltool_name + '_cc.json', 'r', encoding='utf-8')
    con_radon_cc = f_radon_cc.read().replace('\n', '').replace('\r', '')
    dic_radon_cc = json.loads(con_radon_cc, strict=False)     
    
    dic_radon = dic_radon_raw.copy()
    for ele in dic_radon_mi:
        dic_radon[ele].update(dic_radon_mi[ele])
        if "rank" in dic_radon[ele]:
            dic_radon[ele]["mi_rank"] = dic_radon[ele].pop("rank")
            
    for ele in dic_radon_hal:
        dic_radon[ele].update(dic_radon_hal[ele])
        if "functions" in dic_radon[ele]:
            dic_radon[ele]["hal_functions"] = dic_radon[ele].pop("functions")
        if "total" in dic_radon[ele]:
            dic_radon[ele]["hal_total"] = dic_radon[ele].pop("total")
    
    for ele in dic_radon_cc:
        dic_radon[ele]["cyclomatic"] = dic_radon_cc[ele]
        
    return dic_radon

if __name__ == "__main__":
    mltool_name = 'sklearn'
    dic_radon = open_json_files(mltool_name)
    with open('./' + mltool_name + '/radon_' + mltool_name + '.json', 'w') as f:
        f.write(json.dumps(dic_radon))