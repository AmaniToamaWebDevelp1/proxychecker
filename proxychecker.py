#!/usr/bin/env python
# coding: utf-8
# Sublist3r v1.0
# By Amani Toama amanitoama570@gmail.com

# modules in standard library
import requests
import time
import re
import argparse
from requests.exceptions import ProxyError, ConnectTimeout
from colorama import Fore, Style, init


def initialize():
    init(autoreset=True)
    parser = argparse.ArgumentParser(description='Check Proxies from a file or a single proxy.')
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('-t', '--txt', help='Text file containing proxies, one per line.')
    group.add_argument('-s', '--single', help="Single proxy URL (e.g., http://10.20.200.13:80)", type=str)
    parser.add_argument('-p', '--protocol',
                        help="Protocol to use with the single proxy (e.g., socks4), if you don't know the protocol type",
                        type=str)
    args = parser.parse_args()
    return args


def print_banner():
    print(rf"""
      {Fore.LIGHTMAGENTA_EX}
      **************************************************************************************************************
  .______   .______        ______   ___   ___ ____    ____      ______  __    __   _______   ______  __  ___  _______ .______      
  |   _  \  |   _  \      /  __  \  \  \ /  / \   \  /   /     /      ||  |  |  | |   ____| /      ||  |/  / |   ____||   _  \     
  |  |_)  | |  |_)  |    |  |  |  |  \  V  /   \   \/   /     |  ,----'|  |__|  | |  |__   |  ,----'|  '  /  |  |__   |  |_)  |    
  |   ___/  |      /     |  |  |  |   >   <     \_    _/      |  |     |   __   | |   __|  |  |     |    <   |   __|  |      /     
  |  |      |  |\  \----.|  `--'  |  /  .  \      |  |        |  `----.|  |  |  | |  |____ |  `----.|  .  \  |  |____ |  |\  \----.
  | _|      | _| `._____| \______/  /__/ \__\     |__|         \______||__|  |__| |_______| \______||__|\__\ |_______|| _| `._____|
                     
      ***************************************************************************************************************               
                      {Style.BRIGHT + Fore.CYAN}# Proxy Checker Tool by Amani Toama  amanitoama570@gmail.com       
      ---------------------------------------------------------------------------------------------------------------- 
      """)


def check_proxy(proxy):
    proxy_type = identify_proxy_type(proxy)
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
        return 'https'
    elif re.match(r'^http://', proxy):
        return 'http'
    elif re.match(r'^socks5://', proxy):
        return 'socks5'
    elif re.match(r'^socks4://', proxy):
        return 'socks4'
    else:
        return 'http'


def main(proxy_file_path=None, single_proxy=None, protocol=None):
    print_banner()
    try:
        if proxy_file_path:
            with open(proxy_file_path, 'r') as file:
                proxies = file.readlines()
            for i,proxy in enumerate(proxies):
                if i == 3:
                    if input(f"{Fore.BLUE}Press 'q' to quit or any other key to continue: ").lower() == 'q':
                     print(f"{Fore.YELLOW}Proxy checking terminated by user.")
                     break
                proxy = proxy.strip()
                if proxy:
                    protocol_type = identify_proxy_type(proxy)
                    status, latency = check_proxy(proxy)
                    if status:
                        print(
                            f"{Fore.GREEN}Proxy {proxy} is working, proxy type {protocol_type}. Latency: {latency:.2f} seconds.")
                    else:
                        print(f"{Fore.RED}Proxy {proxy} is not working.")
        elif single_proxy:
            protocol_type = protocol if protocol else identify_proxy_type(single_proxy)
            status, latency = check_proxy(single_proxy)
            if status:
                print(
                    f"{Fore.GREEN}Proxy {single_proxy} is working, proxy type {protocol_type}. Latency: {latency:.2f} seconds.")
            else:
                print(f"{Fore.RED}Proxy {single_proxy} is not working.")
        else:
            print(f"{Fore.RED}No proxy information provided.")
    except FileNotFoundError:
        print(f"{Fore.RED}File {proxy_file_path} not found.")


if __name__ == "__main__":
    args = initialize()
    if args.single:
        if args.protocol == "none":
            args.protocol = identify_proxy_type(args.single)
        main(single_proxy=args.single, protocol=args.protocol)
    elif args.txt:
        main(proxy_file_path=args.txt)
