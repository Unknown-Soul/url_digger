# url_digger
Python version of gau with some upgrades
Crawl wayback_machine, AlieVault and CommonCrawler to dig urls
Other than that it also dif for subdomains from same url and crt.sh



usage: Url_Digger.py [-h] -d DOMAIN -l LIMIT -f FILE [-sub] [-sf SUBDOMAIN_FILE]


optional arguments:

-h, --help                                             show this help message and exit

-d DOMAIN, --domain DOMAIN                             The domain to target ie. cnn.com

-l LIMIT, --limit LIMIT                                Number Of Data From Each Url

-f FILE, --file FILE                                   File name eg. test.txt

-sub, --subdomain                                      extract Subdomain

-sf SUBDOMAIN_FILE,  --subdomain_file SUBDOMAIN_FILE   extracted Subdomain and stored in this file
