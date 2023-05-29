# ipv4_parser

## 功能：
将IP地址段、IP地址区间、单个的IP地址解析成IP地址，并返回包含这些IP地址的列表，可以接受多种类型的IP地址或IP地址区间写法，IP地址或范围之间使用英文逗号分隔。
不如 IPy模块 和 ipaddress模块 的方法多，但是比这两个方法支持的IP地址范围写法灵活。

# 用法：
## 直接使用：
    python ipv4_parser.py 192.168.1.1,192.168.10.1/30,192.168.20.10-11,192.168.30.1-192.168.30.10,192.168.40.8/255.255.255.248
![image](https://github.com/defaultuser789/ipv4_parser/assets/38456731/bf07494b-39c3-4b9a-be49-551cf599bc55)

    
## 在其他 python 代码中引用


import ipv4_parser
ips = "192.168.1.1,192.168.10.1/30,192.168.20.10-11,192.168.30.1-192.168.30.10,192.168.40.8/255.255.255.248"
ip_list = ipv4_parser.ipv4_parser(ips)
for ip in ip_list:
    print(ip)
