# -*- encoding -*-
from urllib.parse import urlparse,urlsplit,urljoin
import json
import os
def load_rules():
    try:
        rules=json.load(open('rules.json',encoding='utf8'))
        return rules
    except Exception as e:
        raise e

def load_domains():
    rules=load_rules()
    domains=rules['allowed_domains']
    return domains

def load_tags():
    rules=load_rules()
    tags=rules['allowed_domains']
    return tags

def load_websites():
    rules=load_rules()
    websites=rules['websites']
    websites=[website for website in websites if website['active']]
    cfg_dict={}
    for website in websites:
        url=website['website']
        cfg_dict[url]=website
    return cfg_dict

def get_schemenetloc(url):
    res=urlparse(url)
    nurl=res.scheme+'://'+res.netloc
    return nurl

def load_timefmts():
    rules=load_rules()
    fmts=rules['time_format']
    return fmts
