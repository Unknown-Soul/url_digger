# url_digger
Python version of gau(https://github.com/lc/gau) with some upgrades
It eliminate duplicacy of url that is one problem with gau. Solved using map.
Crawl wayback_machine, AlieVault and CommonCrawler to dig urls
Other than that it also dig for subdomains from same urls and crt.sh. As urls dig from these sources are rich in subdomains 



usage: Url_Digger.py [-h] -d DOMAIN -l LIMIT -f FILE [-sub] [-sf SUBDOMAIN_FILE]


optional arguments:

-h, --help                                             show this help message and exit

-d DOMAIN, --domain DOMAIN                             The domain to target ie. cnn.com

-l LIMIT, --limit LIMIT                                Number Of Data From Each Url

-f FILE, --file FILE                                   File name eg. test.txt

-sub, --subdomain                                      extract Subdomain

-sf SUBDOMAIN_FILE,  --subdomain_file SUBDOMAIN_FILE   extracted Subdomain and stored in this file
