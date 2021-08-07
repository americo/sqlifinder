import requests
import re
import argparse
import os
import sys
import time
import requests
import string

from huepy import *
from core import requester
from core import extractor
from core import crawler
from urllib.parse import unquote
from tqdm import tqdm 

start_time = time.time()

def clear():
    if 'linux' in sys.platform:
        os.system('clear')
    elif 'darwin' in sys.platform:
        os.system('clear')
    else:
        os.system('cls')

def banner():
    ban = '''
            ___ ____         __       
  ___ ___ _/ (_) _(_)__  ___/ /__ ____
 (_-</ _ `/ / / _/ / _ \/ _  / -_) __/
/___/\_, /_/_/_//_/_//_/\_,_/\__/_/   
      /_/        ~ by @americo        v1.0 
      '''

    print(green(ban))

def concatenate_list_data(list, result):
    for element in list:
        result = result + "\n" + str(element)
    return result

def main():
    parser = argparse.ArgumentParser(description='xssfinder - a xss scanner tool')
    parser.add_argument('-d', '--domain', help = 'Domain name of the target [ex. example.com]', required=True)
    parser.add_argument('-s', '--subs', help = 'Set false or true [ex: --subs False]', default=False)
    args = parser.parse_args()

    if args.subs == True:
        url = f"http://web.archive.org/cdx/search/cdx?url=*.{args.domain}/*&output=txt&fl=original&collapse=urlkey&page=/"
    else:
        url = f"http://web.archive.org/cdx/search/cdx?url={args.domain}/*&output=txt&fl=original&collapse=urlkey&page=/"

    '''for i in tqdm (range (100), desc="Starting..."): 
        time.sleep(0.01)'''

    clear()
    banner()

    response = requester.connector(url)
    crawled_urls = crawler.spider(f"http://{args.domain}", 10)
    response = concatenate_list_data(crawled_urls, response)
    if response == False:
        return
    response = unquote(response)

    print("\n"+"["+blue("INF")+"]"+f" Scanning sql injection for {args.domain}")
    
    exclude = ['woff', 'js', 'ttf', 'otf', 'eot', 'svg', 'png', 'jpg']
    final_uris = extractor.param_extract(response , "high", exclude, "")

    file = open('payloads.txt', 'r')
    payloads = file.read().splitlines()

    vulnerable_urls = []

    for uri in final_uris:
        for payload in payloads:
            final_url = uri+payload
            
            try:
                req = requests.get("{}".format(final_url))
                res = req.text
                if 'SQL' in res or 'sql' in res or 'Sql' in res:
                    print("["+green("sql-injection")+"] "+final_url)
                    break                           
            except:
                pass

if __name__ == "__main__":
    clear()
    banner()
    main()