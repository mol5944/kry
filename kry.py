#modules
import requests
from sys import argv
from os.path import exists
from threading import Thread
from time import sleep
from re import search

#def
def help():
    print('--help (display help menu)')
    print('--url (enter site url to scan)')
    print('--wordlist (list of words to scan)')
    print('--threads (threads to scan)')
    print('--sleep_thr (delay between threads)')
    print('--proxy_file (use proxy for scanning)')
    print('--timeout (waiting for a response between requests)')
    print('--search_title (keyword search)')
    print('--verbose (verbose output)')
    print('--output (report output file)')
    print('--good_code (error code)')
    quit()

def generator(string):
    for word in string:
        folder = word.replace('\n','')
        yield folder

def save_url(file_name,url):
    with open(file_name,'at') as file:
        file.write(url + '\n')

def request(url,timeout,proxies,title):
    try:
        resp = requests.get(url,timeout=timeout,proxies=proxies,headers={'User-Agent':'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/78.0.3904.108 Chrome/78.0.3904.108 Safari/537.36'})
    except:
        pass
    else:

        if resp.text == '':
            return

        if resp.status_code == good_code:
            if title != None:
                if search(title,resp.text) != None:
                    return
            if '--verbose' in argv:
                print(url)
            if output[0]:
                save_url(output[1],url)







#argv
if '--help' in argv:
    help()

if '--timeout' in argv:
    timeout = int(argv[argv.index('--timeout') +1])
else:
    timeout = None

if '--proxy_file' in argv:
    with open(argv[argv.index('--proxy_file') + 1],'rt') as file:
        proxy = file.read().split('\n')
        if proxy[-1] == '':
            proxy.pop(-1)
        count_proxy = len(proxy) -1
        count_start_proxy = 0
else:
    proxy=None

if '--url' in argv:
    url = argv[argv.index('--url') +1]
    try:
        requests.get(url,timeout=timeout)
    except:
        print('could not connect to the site')
        quit()

    if url[-1] == '/':
        url = url[0:-1]
else:
    print('########################################')
    print('specify the parameter \'--url\'')
    print('########################################')
    help()

if '--wordlist' in argv:
    wordlist = argv[argv.index('--wordlist') + 1]
    if not exists(wordlist):
        print('could not find a list of words')
        quit()
else:
    print('########################################')
    print('specify the parameter \'--wordlist\'')
    print('########################################')
    help()

if '--output' in argv:
    output = [True,argv[argv.index('--output') +1]]
else:
    output = [False]

if '--good_code' in argv:
    good_code = int(argv[argv.index('--good_code') + 1])
else:
    good_code = 200

if '--threads' in argv:
    threads = int(argv[argv.index('--threads') + 1])
else:
    threads = 1

if '--sleep_thr' in argv:
    sleep_thr = int(argv[argv.index('--sleep_thr') + 1])
else:
    sleep_thr = 0

if '--search_title' in argv:
    title = argv[argv.index('--search_title') +1]
else:
    title = None








count = 0

with open(wordlist,'rt',errors='ignore') as dictionary:
    for folder_url in generator(dictionary):
        check_url = url + '/' + folder_url
        
        if count > threads:
            count = 0
            sleep(sleep_thr)
        else:
            if proxy != None:
                if count_start_proxy > count_proxy:
                    count_start_proxy = 0
                proxies = proxy[count_start_proxy]
                count_start_proxy += 1

                proxies = {'http':'http://' + proxies, 'https':'https://' + proxies}
                
                thr = Thread(target=request, args=(check_url,timeout,proxies,title,))
                thr.start()
                count += 1
            else:
                thr = Thread(target=request, args=(check_url,timeout,None,title,))
                thr.start()
                count += 1







