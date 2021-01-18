#!/usr/bin/python3
import requests
import argparse
import time
import json
import gzip
import csv
import codecs
from bs4 import BeautifulSoup
import urllib
from urllib.request import urlopen
import tldextract


ap = argparse.ArgumentParser()
ap.add_argument("-d", "--domain", required=True,
                help="The domain to target ie. cnn.com")

ap.add_argument("-l", "--limit", required=True,
                help="Number Of Data From Each Url")

ap.add_argument("-f", "--file", required=True,
                help="File name eg.  test.txt")

ap.add_argument("-sub", "--subdomain",
                help="extract Subdomain" ,action="store_true")

ap.add_argument("-sf", "--subdomain_file",
                help="extracted Subdomain and stored in this file")

args = vars(ap.parse_args())   


if("subdomain" in args  and 
    "subdomain_file" not in args or "subdomain_file" == None):
        parser.error('please enter filename of subdomain') 


domain = args['domain']
limit = args['limit']
file_1 = args['file']
file_2 = args['subdomain_file']
subdomain = args['subdomain']

dict = {}
subdomain_dict = {}

#---------------------------------------------------OTX---------------------------------------
AlienVault_url = "https://otx.alienvault.com/api/v1/indicators/domain/%s/passive_dns" %domain
AlienVault_url += "?limit=%s"%limit
response_one = requests.get(AlienVault_url)
record_list= []
passive_dns_list = []
if response_one.status_code == 200:
            records_one = response_one.content.splitlines()
            for record in records_one:
                for x in range(0,(int)(json.loads(record)['count'])):
                    out = json.loads(record)["passive_dns"][x]['hostname']
                    passive_dns_list.append(out)
                    if out in dict.keys():
                        dict[out] = (int(dict[out]) + 1)
                    else:
                        dict[out] = 1
                    if subdomain == True:
                        if(out.endswith("vtm.be") and not out.startswith("*")):
                            if out in subdomain_dict.keys():
                                subdomain_dict[out] = (int(subdomain_dict[out]) + 1)
                            else:
                                subdomain_dict[out] = 1
                    


url2 = 'https://otx.alienvault.com/api/v1/indicators/domain/%s/url_list'%domain
response = requests.get(url2)
if response.status_code == 200:
            records = response.content.splitlines()
            size = json.loads(records[0].decode('utf-8'))['full_size']
            url2 += '?limit=%d'%size
            print(url2)
            response = requests.get(url2)
            records = response.content.splitlines()
            if response.status_code == 200:
                for x in range(1,50):
                    out1 =json.loads(records[0].decode('utf-8'))['url_list'][x]['url']
                    out2 =json.loads(records[0].decode('utf-8'))['url_list'][x]['hostname']
                    record_list.append(out1)
                    record_list.append(out2)
                    if out1 in dict.keys():
                        dict[out1] = (int(dict[out1]) + 1)
                    else:
                        dict[out1] = 1

                    if out2 in dict.keys():
                        dict[out2] = (int(dict[out2]) + 1)
                    else:
                        dict[out2] = 1

                    if subdomain == True:
                        if(out1.endswith("vtm.be") and not out1.startswith("*")):
                            if out1 in subdomain_dict.keys():
                                subdomain_dict[out1] = (int(subdomain_dict[out1]) + 1)
                            else:
                                subdomain_dict[out1] = 1
                        if(out2.endswith("vtm.be") and not out2.startswith("*")):
                            if out2 in subdomain_dict.keys():
                                subdomain_dict[out2] = (int(subdomain_dict[out2]) + 1)
                            else:
                                subdomain_dict[out2] = 1                

#----------------------------------------------Wayback_Scraper-------------------------------------

wayback_list = []
URL = "http://web.archive.org/cdx/search/cdx?url=%s&matchType=domain&fl=original&collapse=urlkey&"%domain
URL += "limit=%s&output=txt"%limit
print(URL)
r = urllib.request.urlopen(URL) 
soup = BeautifulSoup(r, 'html5lib') 
soup.prettify()
data = soup.body.text
for x in data.split():
    if x in dict.keys():
        dict[x] = (int(dict[x]) + 1)
    else:
        dict[x] = 1

    if subdomain == True:
        if(x.endswith("vtm.be") and not x.startswith("*")):
                            if x in subdomain_dict.keys():
                                subdomain_dict[x] = (int(subdomain_dict[x]) + 1)
                            else:
                                subdomain_dict[x] = 1    

#----------------------------------------Comman Crawler--------------------------------------------


# list of available indices
index_list = []
index_url = "https://index.commoncrawl.org/collinfo.json"
ruh = urllib.request.urlopen(index_url)
data = ruh.read()
info = json.loads(data)

for i in info:
    da = i['id']
    index_list.append(da[8:16])


index_list = ['2015-18','2014-42']
for index in index_list:
        cc_url = "http://index.commoncrawl.org/CC-MAIN-%s-index?" % index
        cc_url += "url=%s&matchType=domain&output=json&" % domain
        cc_url += "limit=%s" %limit 
        print(cc_url)
        response = requests.get(cc_url)
        if response.status_code == 200:
            records = response.content.splitlines()
            for record in records:
                data = json.loads(record)["url"]
                if data in dict.keys():
                    dict[data] = (int(dict[data]) + 1)
                else:
                    dict[data] = 1    
                if subdomain == True:
                        if(data.endswith("vtm.be") and not data.startswith("*")):
                            if data in subdomain_dict.keys():
                                subdomain_dict[data] = (int(subdomain_dict[data]) + 1)
                            else:
                                subdomain_dict[data] = 1    
                        ext = tldextract.extract(data)
                        if(ext.subdomain != ""):
                            final = ext.subdomain+"."+ext.domain+"."+ext.suffix
                            if final in subdomain_dict.keys():
                                subdomain_dict[final] = (int(subdomain_dict[final]) + 1)
                            else:
                                subdomain_dict[final] = 1   



#for key,value in dict.items():
    #print('{} : {}'.format(key, value))
for x in dict:
    file2 = open(file_1, 'a')
    file2.write(x)
    file2.write(f"\n")
    file2.close()    

#-------------------------------------------Sub_Domain------------------------------------------------
if subdomain == True:
    crt_url = "https://crt.sh/?q=%s"%domain
    r = requests.get(crt_url) 
    soup = BeautifulSoup(r.content, 'html5lib')    
    print(crt_url)

    for tr in soup.find_all('tr')[1:]:
            tds = tr.find_all('td')
            if len(tds) == 7:
                data = (tds[5].find(text=True))
                if(data.endswith("vtm.be") and not data.startswith("*")):
                    if data in subdomain_dict.keys():
                        subdomain_dict[data] = (int(subdomain_dict[data]) + 1)
                    else:
                        subdomain_dict[data] = 1    
                data = (tds[4].find(text=True))
                if(data.endswith("vtm.be") and not data.startswith("*")):
                    if data in subdomain_dict.keys():
                        subdomain_dict[data] = (int(subdomain_dict[data]) + 1)
                    else:
                        subdomain_dict[data] = 1


    for x in subdomain_dict:
        file2 = open(file_2, 'a')
        file2.write(x)
        file2.write(f"\n")
        file2.close()    
