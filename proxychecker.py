#!/usr/bin/env python
# coding: utf-8
# PROXY Checker v0.1.0
# By Amani Toama amanitoama570@gmail.com
from itertools import count

# modules in standard library
import requests
import time
import re
import argparse
from requests.exceptions import ProxyError, ConnectTimeout
from colorama import Fore, Style, init
import sys
import  signal
init()

def initialize():
    init(autoreset=True)
    parser = argparse.ArgumentParser(description='Check Proxies from a file or a single proxy.')
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('-t', '--txt', help='Text file containing proxies, one per line.')
    group.add_argument('-s', '--single', help="Single proxy URL (e.g., http://10.20.200.13:80)", type=str)
    parser.add_argument('-p', '--protocol',
                        help="Protocol to use with the single proxy (e.g., socks4), if you don't know the protocol type none",
                        type=str, default="http")
    args = parser.parse_args()
    return args

# ctrl + c interrupting
def signal_handler(sig, frame):
    print(f'\nYou pressed Ctrl+C! Exiting Code 0 \n')
    # Perform any cleanup if needed
    sys.exit(0)
def print_banner():
    print(rf"""
      {Fore.LIGHTMAGENTA_EX}


  _____   ______  _____  _     _ __   __      _______ _     _ _______ _______ _     _ _______  ______
 |_____] |_____/ |     |  \___/    \_/        |       |_____| |______ |       |____/  |______ |_____/
 |       |    \_ |_____| _/   \_    |         |_____  |     | |______ |_____  |    \_ |______ |    \_
                                                                                                     

 
{Style.DIM}{Fore.CYAN}# Proxy Checker Tool by Amani Toama  amanitoama570@gmail.com
 --------------------------------------------------------------------------
 """)

# extract ip func
def extract_ip(address):
    ip = address.split(':')[0]
    return ip

# country detective func
def get_ip_country(ip):
    res = requests.get(f"http://ip-api.com/json/{ip}")
    data = res.json()
    if res.status_code == 200:
        return data['country']
    else:
        return "error"

def check_proxy(proxy, proxy_type):
    proxies = {proxy_type: proxy}
    try:
        start_time = time.time()
        response = requests.get('http://httpbin.org/ip', proxies=proxies, timeout=5)
        end_time = time.time()
        if response.status_code == 200:
            latency = end_time - start_time
            return True, latency
    except (ProxyError, ConnectTimeout, requests.exceptions.RequestException):
        return False, None
    return False, None


def identify_proxy_type(proxy):
    if re.match(r'^https?://', proxy):
        return 'http'
    elif re.match(r'^http://', proxy):
        return 'http'
    elif re.match(r'^socks5://', proxy):
        return 'socks5'
    elif re.match(r'^socks4://', proxy):
        return 'socks4'
    else:
        return 'http'

print_banner()

def main(proxy_file_path=None, single_proxy=None, protocol=None):
    signal.signal(signal.SIGINT, signal_handler)
    print(f"{Style.RESET_ALL}{Fore.WHITE}Checking Proxy... ")
    print(rf"""{Fore.YELLOW}
   ___________________________________________________________________________________________
                PROXY              |       Latency       |    Status    |      Country       
  --------------------------------------------------------------------------------------------
                          """)
    try:
        if proxy_file_path:
            with open(proxy_file_path, 'r') as file:
                proxies = file.readlines()
            for i, proxy in enumerate(proxies):
                proxy = proxy.strip()
                ip = extract_ip(proxy)
                cntry = get_ip_country(ip)

                if proxy:
                    status, latency = check_proxy(proxy, identify_proxy_type(proxy))
                    if status:
                        print(
                            f"{Fore.GREEN}  {proxy:^32} |     {latency:.2f}sec         |    {'True' if status else 'False':<9} | {cntry:^15}  ")
                    else:
                        print(
                            f"{Fore.RED}  {proxy:^32} | {'---':^17}   |    {'True' if status else 'False':<9} | {cntry:^15}  ")
                if (i + 1) % 10 == 0:  # Every 10 proxies, ask to continue or terminate
                    if input(f"{Fore.BLUE}Press 'q' to quit or any other key to continue: ").lower() == 'q':
                        print(f"{Fore.YELLOW}Proxy checking terminated by user.")
                        break 
                        sys.exit(0)
        elif single_proxy:
            protocol_type = protocol if protocol else identify_proxy_type(single_proxy)
            cntry = get_ip_country(extract_ip(single_proxy))
            status, latency = check_proxy(single_proxy, protocol_type)
            if status:
                print(f"{Fore.GREEN}Proxy {single_proxy} is working. Latency: {latency:.2f} seconds. Country: {cntry}")
            else:
                print(
                    f"{Fore.RED}  {single_proxy:^32} | {'---':^17}   |    {'True' if status else 'False':<9} | {cntry:^15}  ")
        else:
            print(f"{Fore.RED}Proxy {single_proxy} is not working.")
    except FileNotFoundError:
        print(f"{Fore.RED}File {proxy_file_path} not found.")

    try:
        while True:
            pass
    except KeyboardInterrupt:
        # Catch KeyboardInterrupt to ensure the program exits gracefully
        print('\nExiting due to Ctrl+C')
        sys.exit(0)


if __name__ == "__main__":
    args = initialize()
    if args.single:
        if args.protocol == "none":
            args.protocol = identify_proxy_type(args.single)
        main(single_proxy=args.single, protocol=args.protocol)
    elif args.txt:
        main(proxy_file_path=args.txt)

