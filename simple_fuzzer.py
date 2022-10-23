from multiprocessing import Pool

import requests, sys, os, argparse

def check_args():

    parser = argparse.ArgumentParser(description="Dir fuzzer",
                                 usage="Script options")
    parser.add_argument("-u", help="Enter domain http://site.com/FUZZ")
    parser.add_argument("-w", help="Name and path of wordlist")
    parser.add_argument("-t", help="Number of threads", type=int) # добавить type=int
    args = parser.parse_args()
    if (args.u == None and args.w == None ):
        parser.print_help()

        return
    targets = check_domain(args.u)
    urls = check_wordlist(args.w)


    threads = args.t
    return targets, urls, threads

def check_wordlist(path):
    urls = []
    if not os.path.exists(path):
        print("File not found")
        sys.exit()

    with open (path,"r") as file:

        for line in file:
            line = line.replace("\n", "")
            urls.append(line)
    return urls



def check_domain(target):
    target = str(target).replace("FUZZ", "")
    try:
        responce = requests.get(target, headers={"User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.119 Safari/537.36"}, timeout=1)
        if responce.status_code == 200:
            return target #
            # -TARGET = target
    except (requests.exceptions.HTTPError, requests.exceptions.Timeout) as e:
        print('ERROR: %s' % e)


def creating_list(target, urls):
    return [f'{target}/{line}' for line in urls]


def start_attack(index, target):
    try:

        responce = requests.get(target, headers={"User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.119 Safari/537.36"}, timeout=1)
        if responce.status_code == 404:
            print(f"{index:08d} , {responce.status_code}" , ":" + target , end = "\r")
        elif responce.status_code == 403:
            print(f"{index:08d} ", '\033[91m', responce.status_code ,  ":" + target + '\033[0m')
        elif responce.status_code == 200:
            print(f"{index:08d} ",'\033[92m', responce.status_code ,  ":" + target + '\033[0m' )

    except KeyboardInterrupt:
        print('\033[31m' + '  ERROR: manually stop Ctrl+C' + '\033[0m')



if __name__ == '__main__':
    targets, urls, threads = check_args()
    urls_list = creating_list(targets,urls)
    try:
        thread = Pool(threads)
        thread.starmap(start_attack, enumerate(urls_list))

    except KeyboardInterrupt:
        print('\033[31m' + '  ERROR: manually stop Ctrl+C' + '\033[0m')
