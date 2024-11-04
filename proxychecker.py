#!/usr/bin/env python
# coding: utf-8
# PROXY Checker v0.1.0
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
                        help="Protocol to use with the single proxy (e.g., socks4), if you don't know the protocol type none",
                        type=str, default="http")
    args = parser.parse_args()
    return args


def print_banner():
    print(rf"""
      {Fore.LIGHTMAGENTA_EX}
************************************************************************
                     
____________ _______   ___   __  _____ _               _             
| ___ \ ___ \  _  \ \ / | \ / / /  __ \ |             | |            
| |_/ / |_/ / | | |\ V / \ V /  | /  \/ |__   ___  ___| | _____ _ __ 
|  __/|    /| | | |/   \  \ /   | |   | '_ \ / _ \/ __| |/ / _ \ '__|
| |   | |\ \\ \_/ / /^\ \ | |   | \__/\ | | |  __/ (__|   <  __/ |   
\_|   \_| \_|\___/\/   \/ \_/    \____/_| |_|\___|\___|_|\_\___|_|   
                                                                     
                                                                     
 *************************************************************************
 {Style.BRIGHT + Fore.CYAN}
# Proxy Checker Tool by Amani Toama  amanitoama570@gmail.com
 --------------------------------------------------------------------------
 {Force.WHITE}Checking Proxy...\n
      """)


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


def main(proxy_file_path=None, single_proxy=None, protocol=None):
    print_banner()
    try:
        if proxy_file_path:
            with open(proxy_file_path, 'r') as file:
                proxies = file.readlines()
            for i, proxy in enumerate(proxies):
                proxy = proxy.strip()
                if proxy:
                    status, latency = check_proxy(proxy, identify_proxy_type(proxy))
                    if status:
                        print(f"{Fore.GREEN}Proxy {proxy} is working. Latency: {latency:.2f} seconds.")
                    else:
                        print(f"{Fore.RED}Proxy {proxy} is not working.")
                if (i + 1) % 10 == 0:  # Every 3 proxies, ask to continue or terminate
                    if input(f"{Fore.BLUE}Press 'q' to quit or any other key to continue: ").lower() == 'q':
                        print(f"{Fore.YELLOW}Proxy checking terminated by user.")
                        break
        elif single_proxy:
            protocol_type = protocol if protocol else identify_proxy_type(single_proxy)
            status, latency = check_proxy(single_proxy, protocol_type)
            if status:
                print(f"{Fore.GREEN}Proxy {single_proxy} is working. Latency: {latency:.2f} seconds.")
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
