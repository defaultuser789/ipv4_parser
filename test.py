# _*_ coding: utf-8 _*_

import ipv4_parser

ips = "192.168.1.10"

ip_list = ipv4_parser.ipv4_parser(ips)

for ip in ip_list:
    print(ip)
