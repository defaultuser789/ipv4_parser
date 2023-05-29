# _*_ coding: utf-8 _*_

import sys
import re


def ipv4_parser(ip_line):
    ret_list = []
    
    ips_list = ip_line.strip()
    for character in ips_list:
        if not re.match('^[0-9|\,|\.|\/|\-]*$', character):
            raise ValueError(f'"{ips_list}": IP 地址列表中包含非法字符，仅限数字、英文点、短横线和正斜线')
            return -1

    ips_list = ips_list.split(',')
    for ips in ips_list:
    
        # 192.168.80.1/24形式
        if re.match('^(\d{1,3}\.){3}\d{1,3}\/\d{1,2}$', ips):
            ip_mask = ips.split('/')
            ip_segments = ip_mask[0].strip().split('.')
            for ip_segment in ip_segments:
                if int(ip_segment) < 0 or int(ip_segment) > 255 or \
                int(ip_mask[1]) < 0 or int(ip_mask[1]) > 32:
                    raise ValueError(f'"{ips}": IP 地址或掩码数值越界')
                    return -1
                    
            ip_segment_index = int(ip_mask[1]) // 8
            ip_segment_offset = int(ip_mask[1]) % 8
            
            for i in range(0, ip_segment_index):
                ip_segments[i] = (int(ip_segments[i]), int(ip_segments[i]))
                
            for j in range(ip_segment_index + 1, 4):
                ip_segments[j] = (0, 255)
                
            if  ip_segment_index != 4:   
                ip_segments[ip_segment_index] = (int(ip_segments[ip_segment_index]) & \
                (0xFF << (8 - ip_segment_offset)),(int(ip_segments[ip_segment_index]) & \
                (0xFF << (8 - ip_segment_offset))) + (0x01 << (8 - ip_segment_offset)) - 1)
                
            for ip_idx_0 in range(int(ip_segments[0][0]),int(ip_segments[0][1])+1):
                for ip_idx_1 in range(int(ip_segments[1][0]),int(ip_segments[1][1])+1):
                    for ip_idx_2 in range(int(ip_segments[2][0]),int(ip_segments[2][1])+1):
                        for ip_idx_3 in range(int(ip_segments[3][0]),int(ip_segments[3][1])+1):
                            ret_list.append(f'{ip_idx_0}.{ip_idx_1}.{ip_idx_2}.{ip_idx_3}')

        # 192.168.80.1/255.255.255.0形式
        elif re.match('^(\d{1,3}\.){3}\d{1,3}\/(\d{1,3}\.){3}\d{1,3}$', ips):
            mask_lists = ['0', '128', '192', '224', '240', '248', '252', '254', '255']
            ip_mask = ips.split('/')
            ip_segments = ip_mask[0].strip().split('.')
            mask_segments = ip_mask[1].strip().split('.')
            for ip_segment in ip_segments:
                if int(ip_segment) < 0 or int(ip_segment) > 255:
                    raise ValueError(f'"{ips}": IP地址数值越界')
                    return -1
            
            for mask_segment in mask_segments:
                if not mask_segment in mask_lists:
                    illegal_ip_flag = 1
                    raise ValueError(f'"{ips}": 掩码数值错误')
                    return -1

            for i in range(0, 3):
                if int(mask_segments[i]) < 255:
                    for j in range(i + 1, 4):
                        if int(mask_segments[j]) > 0:
                            raise ValueError(f'"{ips}": 掩码格式错误')
                            return -1
                            
            for i in range(0, 4):
                if int(mask_segments[i]) == 0:
                    ip_segments[i] = (0, 255)
                
                elif int(mask_segments[i]) == 255:
                    ip_segments[i] = (int(ip_segments[i]) & int(mask_segments[i]), \
                    int(ip_segments[i]) & int(mask_segments[i]))
                    
                else:
                    ip_segments[i] = (int(ip_segments[i]) & int(mask_segments[i]), \
                    (int(ip_segments[i])&int(mask_segments[i])) + 255 - int(mask_segments[i]))
            
            for ip_idx_0 in range(int(ip_segments[0][0]),int(ip_segments[0][1])+1):
                for ip_idx_1 in range(int(ip_segments[1][0]),int(ip_segments[1][1])+1):
                    for ip_idx_2 in range(int(ip_segments[2][0]),int(ip_segments[2][1])+1):
                        for ip_idx_3 in range(int(ip_segments[3][0]),int(ip_segments[3][1])+1):
                            ret_list.append(f'{ip_idx_0}.{ip_idx_1}.{ip_idx_2}.{ip_idx_3}')

        # 192.168.80.1-100 形式
        elif re.match('^(\d{1,3}\.){3}\d{1,3}\-\d{1,3}$', ips):
            ip_range = ips.strip().split('-')
            ip_segments = ip_range[0].strip().split('.')
            
            ip_start_index = 0
            ip_end_index = 0
            if int(ip_range[1]) >= int(ip_segments[3]) and int(ip_range[1]) < 256:
                ip_start_index = int(ip_segments[3])
                ip_end_index = int(ip_range[1])
                
            else:
                raise ValueError(f'"{ips}": IP 地址范围错误')
                return -1
            
            for ip_index in range(ip_start_index,ip_end_index + 1):
                ret_list.append(f'{ip_segments[0]}.{ip_segments[1]}.{ip_segments[2]}.{ip_index}')
            
            
        # 192.168.8.1-192.168.8.100 形式       
        elif re.match('^(\d{1,3}\.){3}\d{1,3}\-(\d{1,3}\.){3}\d{1,3}$', ips):
        
            ip_range = ips.strip().split('-')
            ip1_range = ip_range[0].strip().split('.')
            ip2_range = ip_range[1].strip().split('.')
            
            ip1_value = ( int(ip1_range[0]) << 24) + (int(ip1_range[1]) << 16) + \
            (int(ip1_range[2]) << 8 ) + int(ip1_range[3] )
            ip2_value = ( int(ip2_range[0]) << 24) + (int(ip2_range[1]) << 16) + \
            (int(ip2_range[2]) << 8 ) + int(ip2_range[3] )

            if ip1_value > ip2_value:
                raise ValueError(f'"{ips}": IP 地址范围错误')
                retrurn -1
            else:
                for i in range(ip1_value, ip2_value + 1):
                    ip_segments = ( (i >> 24) % 256, (i >> 16) % 256, \
                    (i >> 8) % 256, i % 256 )
                    ret_list.append(
                        f'{ip_segments[0]}.{ip_segments[1]}.{ip_segments[2]}.{ip_segments[3]}'
                    )

        # 192.168.80.1 形式
        elif re.match('^(\d{1,3}\.){3}\d{1,3}$', ips):
            
            ip = ips.strip() 
            ip_segments = ip.split('.')
                        
            ret_list.append(
                f'{int(ip_segments[0])}.{int(ip_segments[1])}.{int(ip_segments[2])}.{int(ip_segments[3])}'
            )
            
        else:
            raise ValueError(f'"{ips}": IP 地址格式或范围错误')
            return -1
    return ret_list


if __name__ == '__main__':

    
    if len(sys.argv) != 2:
        print('命令格式错误，使用方法：python3 "IP_list"')
        
    else:
        ips = sys.argv[1]
        
        print(ipv4_parser(ips))
        
