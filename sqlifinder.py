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

def main():
    parser = argparse.ArgumentParser(description='xssfinder - a xss scanner tool')
    parser.add_argument('-d', '--domain', help = 'Domain name of the target [ex. example.com]', required=True)
    parser.add_argument('-s', '--subs', help = 'Set false or true [ex: --subs False]', default=False)
    args = parser.parse_args()

    if args.subs == True:
        url = f"http://web.archive.org/cdx/search/cdx?url=*.{args.domain}/*&output=txt&fl=original&collapse=urlkey&page=/"
    else:
        url = f"http://web.archive.org/cdx/search/cdx?url={args.domain}/*&output=txt&fl=original&collapse=urlkey&page=/"

    for i in tqdm (range (100), desc="Starting..."): 
        time.sleep(0.01)

    clear()
    banner()

    print(green("target: ")+args.domain)

    response = requester.connector(url)
    if response == False:
        return
    response = unquote(response)

    print("\n[*] scanning the target...")

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
                if 'SQL' in res:
                    print(green("[!] sql injection found at: ")+final_url)
                    break
                elif 'sql' in res:
                    print(green("[!] sql injection found at: ")+final_url)
                    break
                elif 'Sql' in res:
                    print(green("[!] sql injection found at: ")+final_url)
                    break
                else:
                    pass                                
            except:
                pass

if __name__ == "__main__":
    clear()
    banner()
    main()