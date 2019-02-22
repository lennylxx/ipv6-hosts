#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#chmod +x ipv6hosts.py && python3 ipv6hosts.py hosts_hk_new_201902 -o hosts_hk_unix -n 20
'''
该版本是我想要修正bug，当hosts文件一行只有一个域名的时候，因为没有检查arr[0]是不是ip
因此会出现
google.com google.com#example
的情况。
我希望在len(arr)的地方做出判断，但是貌似计数的进程会出现问题。
我也不知道为什么
'''
import os
import sys
import re
import socket
import ipaddress
import getopt
import threading
import subprocess
import shlex
import time
import select
import requests
blackhole = (
    '10::2222',
    '21:2::2',
    '101::1234',
    '200:2:807:c62d::',
    '200:2:253d:369e::',
    '200:2:2e52:ae44::',
    '200:2:3b18:3ad::',
    '200:2:4e10:310f::',
    '200:2:5d2e:859::',
    '200:2:9f6a:794b::',
    '200:2:cb62:741::',
    '200:2:cc9b:953e::',
    '200:2:f3b9:bb27::',
    '2001::212',
    '2001:da8:112::21ae',
    '2003:ff:1:2:3:4:5fff:6',
    '2003:ff:1:2:3:4:5fff:7',
    '2003:ff:1:2:3:4:5fff:8',
    '2003:ff:1:2:3:4:5fff:9',
    '2003:ff:1:2:3:4:5fff:10',
    '2003:ff:1:2:3:4:5fff:11',
    '2003:ff:1:2:3:4:5fff:12',
    '2123::3e12',
    '3059:83eb::e015:2bee:0:0',
    '1.2.3.4',
    '4.36.66.178',
    '8.7.198.45',
    '37.61.54.158',
    '46.82.174.68',
    '59.24.3.173',
    '64.33.88.161',
    '78.16.49.15',
    '93.46.8.89',
    '127.0.0.1',
    '159.106.121.75',
    '202.181.7.85',
    '203.98.7.65',
    '243.185.187.39'
)

invalid_network = [
    '200:2::/32',
    '2001::/32', #TEREDO
    'a000::/8',
]

dns = {
    'google_a': '2001:4860:4860::8888',
    'google_b': '2001:4860:4860::8844',
    'he_net': '2001:470:20::2',
    'lax_he_net': '2001:470:0:9d::2'
}

config = {
    'dns': dns['google_b'],
    'infile': '',
    'outfile': '',
    'querytype': 'aaaa',
    'cname': False,
    'threadnum': 10
}


hosts = []
done_num = 0
thread_lock = threading.Lock()
running = True

class worker_thread(threading.Thread):
    def __init__(self, start_pt, end_pt):
        threading.Thread.__init__(self)
        self.start_pt = start_pt
        self.end_pt = end_pt

    def run(self):
        global hosts, done_num
        for i in range(self.start_pt, self.end_pt):
            if not running: break

            line = hosts[i].strip()

            if line == '' or line[0:2] == '##':
                hosts[i] = line + '\r\n'
                with thread_lock: done_num += 1
                continue

            # uncomment line
            line = line.lstrip('#')
            # split comment that appended to line
            comment = ''
            p = line.find('#')
            if p > 0:
                comment = line[p:]
                line = line[:p]
            arr = line.split()
            ip=''
            if len(arr) == 1:
                domain = arr[0]
                if validate_domain(domain):
                    ip = query_domain(domain, False)
                
            else:
                domain = arr[1]
                if validate_domain(domain):
                    tcp_flag=ip_available(arr[0])
                    if tcp_flag==0:
                        ip=arr[0]
                    else:
                        ip = query_domain(domain, False)
                
           

                # if ip == '' or ip in blackhole or invalid_address(ip):
                    # ip = query_domain(domain, True)

            if ip:
                #flag = True
                arr[0] = ip
                if len(arr) == 1:
                    arr.append(domain)
                # if config['cname'] and cname:
                    # arr.append('#' + cname)
                else:
                    if comment:
                        arr.append(comment)
            else:
                arr[0] = '#' + arr[0]
                if comment:
                    arr.append(comment)


        # if not flag:
            # arr[0] = '#' + arr[0]
            # if comment:
                # arr.append(comment)

        hosts[i] = ' '.join(arr)
        hosts[i] += '\r\n'
        with thread_lock: done_num += 1

class watcher_thread(threading.Thread):
    def run(self):
        total_num = len(hosts)

        wn = int(config['threadnum'])
        if wn > total_num:
            wn = total_num
        print("There are %d threads working..." % wn)
        print("Press 'Enter' to exit.\n")

        while True:
            if sys.stdin in select.select([sys.stdin], [], [], 0)[0]:
                input()
                print("Waiting threads to exit...")
                global running
                with thread_lock:
                    running = False
                break

            dn = done_num
            outbuf = "Total: %d lines, Done: %d lines, Ratio: %d %%.\r"\
                     % (total_num, dn, dn * 100 / total_num)
            print(outbuf, end='', flush=True)

            if dn == total_num:
                print(outbuf)
                break

            time.sleep(1)

'''
看起来查询函数就是下面这个函数，只需要将dig用支持edns的换掉，然后在这个命令加入判断是否被墙的模块
dig -6                  (use IPv6 query transport only)
但是我不明白怎么会使，貌似也可以用ipv6的dns呢。但是改成-4 就没法用ipv6地址的dns了，所以也是很神奇的事情啊
dig +short +time=2 +tries=5 -6 -t aaaa @2001:4860:4860::8888 www.google.com 

curl -H 'accept: application/dns-json' 'https://dns.google.com/resolve?name=www.google.com&type=AAAA'

curl -H 'accept: application/dns-json' 'https://dns.google.com/resolve?name=www.google.com&type=AAAA&edns_client_subnet=175.45.20.138'

curl -6 -s 'https://dns.google.com/resolve?name=www.google.com&type=AAAA&edns_client_subnet=175.45.20.138' | python -m json.tool

'''

'''
import json
json_data=os.system('curl -6 -s 'https://dns.google.com/resolve?name=15.sn-bvvbax-hn2d.googlevideo.com&type=AAAA&edns_client_subnet=175.45.20.138'')
data = json.loads(json_data)
print('%s'%data['Answer']['date'])
# for v in data['favourite']['bkmrk'].values():
    # print("%s;%s" % (v['lcate'],  v['guid']))
requests.get('https://dns.google.com/resolve?name=%s&type=%s&edns_client_subnet=175.45.20.138'%('15.sn-bvvbax-hn2d.googlevideo.com','aaaa')).json()['Answer'][0]['data']
requests.get('https://dns.google.com/resolve?name=%s&type=%s&edns_client_subnet=175.45.20.138'%('googlevideo.com','aaaa')).json()['Answer'][0]['data']
requests.get('https://dns.rubyfish.cn/dns-query?name=%s&type=%s'%('blog.google','aaaa')).json()['Answer'][0]['data']

https://dns.rubyfish.cn/dns-query?name=www.google.com&type=A'
'''
def query_domain(domain, tcp):
    # cmd = "dig +short +time=2 -6 %s @'%s' '%s'"\
        # % (config['querytype'], config['dns'], domain)

    # if tcp:
        # cmd = cmd + ' +tcp'

    # proc = subprocess.Popen(shlex.split(cmd), stdout=subprocess.PIPE)
    # out, _ = proc.communicate()
    # outarr = out.decode('utf-8').splitlines()

    # cname = ip = ''
    # for v in outarr:
        # if cname == '' and validate_domain(v[:-1]):
            # cname = v[:-1]
        # if ip == '' and validate_ip_addr(v):
            # ip = v
            # break


    
    counter=0
    code=2
    
    while(counter<6):
        if counter==0 or counter==1 or counter==2:
            ipad='202.40.161.203'
        elif counter==3:
            ipad='134.208.0.0'
        elif counter==4:
            ipad='115.85.29.130'
        else:
            ipad='155.69.203.4'
        
     
        url = 'https://dns.google.com/resolve?name=%s&type=%s&edns_client_subnet=%s'%(domain,config['querytype'],ipad)
        counter=counter+1
        r = requests.get(url)
        code=r.status_code
        if code == 200 : #int
            rj=r.json()
            if 'Answer' in rj:
                for pos in rj['Answer']:
                    if 'data' in pos:
                        ip=pos['data']
                        www=pos['name']
                        tcp_flag=ip_available(ip)
                        if tcp_flag==0:
                            return ip
                
                # if validate_ip_addr(ip):
                    # s = socket.socket(socket.AF_INET6, socket.SOCK_STREAM)
                    # s.settimeout(1)
                    # tcp_flag=s.connect_ex((ip, 443))
            else:
                break
    return
         
            
                
                
                
    
'''
import socket
s = socket.socket(socket.AF_INET6, socket.SOCK_STREAM)
s.connect(('2404:6800:4005:80e::200e', 80))

检测状态，超时时间要设置,能够返回error或者success，success是0，socket.SOCK_STREAM是TCP连接
s.settimeout(1)
s.connect_ex(('2404:6800:4005:80e::200e', 443))
s.connect_ex(('2404:6800:4005:808::200e', 443))
s.connect_ex(('2404:6800:4005:800::2003', 443))
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
socket.timeout: timed out
'''
def ip_available(ip):
    if validate_ip_addr(ip):
        s = socket.socket(socket.AF_INET6, socket.SOCK_STREAM)
        s.settimeout(2)
        tcp_flag=s.connect_ex((ip, 443))
        s.close()
        return tcp_flag
    
    

def validate_domain(domain):
    pattern = '^((?!-)[*A-Za-z0-9-]{1,63}(?<!-)\\.)+[A-Za-z]{2,6}$'
    p = re.compile(pattern)
    m = p.match(domain)
    if m:
        return True
    else:
        return False

def validate_ip_addr(ip_addr):
    if ':' in ip_addr:
        try:
            socket.inet_pton(socket.AF_INET6, ip_addr)
            return True
        except socket.error:
            return False
    else:
        try:
            socket.inet_pton(socket.AF_INET, ip_addr)
            return True
        except socket.error:
            return False

def invalid_address(ip_addr):
    address = ipaddress.ip_address(ip_addr)
    for cidr in invalid_network:
        if address in ipaddress.ip_network(cidr):
            return True
    else:
        return False

def print_help():
    print('''usage: update_hosts [OPTIONS] FILE
A simple multi-threading tool used for updating hosts file.

Options:
  -h, --help             show this help message and exit
  -s DNS                 set another dns server, default: 2001:4860:4860::8844
  -o OUT_FILE            output file, default: inputfilename.out
  -t QUERY_TYPE          dig command query type, default: aaaa
  -c, --cname            write canonical name into hosts file
  -n THREAD_NUM          set the number of worker threads, default: 10
''')

def get_config():
    shortopts = 'hs:o:t:n:c'
    longopts = ['help', 'cname']

    try:
        optlist, args = getopt.gnu_getopt(sys.argv[1:], shortopts, longopts)
    except getopt.GetoptError as e:
        print(e)
        print_help()
        sys.exit(1)

    global config
    for key, value in optlist:
        if key == '-s':
            config['dns'] = value
        elif key == '-o':
            config['outfile'] = value
        elif key == '-t':
            config['querytype'] = value
        elif key in ('-c', '--cname'):
            config['cname'] = True
        elif key == '-n':
            config['threadnum'] = int(value)
        elif key in ('-h', '--help'):
            print_help()
            sys.exit(0)

    if len(args) != 1:
        print("You must specify the input hosts file (only one).")
        sys.exit(1)

    config['infile'] = args[0]
    if config['outfile'] == '':
        config['outfile'] = config['infile'] + '.out'

def main():
    get_config()

    dig_path = '/usr/bin/dig'
    if not os.path.isfile(dig_path) or not os.access(dig_path, os.X_OK):
        print("It seems you don't have 'dig' command installed properly "\
              "on your system.")
        sys.exit(2)

    global hosts
    try:
        with open(config['infile'], 'r') as infile:
            hosts = infile.readlines()
    except IOError as e:
        print(e)
        sys.exit(e.errno)

    if os.path.exists(config['outfile']):
        config['outfile'] += '.new'

    try:
        outfile = open(config['outfile'], 'w')
    except IOError as e:
        print(e)
        sys.exit(e.errno)

    print("Input: %s    Output: %s\n" % (config['infile'], config['outfile']))

    threads = []

    t = watcher_thread()
    t.start()
    threads.append(t)

    worker_num = config['threadnum']
    lines_num = len(hosts)

    lines_per_thread = lines_num // worker_num
    lines_remain = lines_num % worker_num

    start_pt = 0

    for _ in range(worker_num):
        if not running: break

        lines_for_thread = lines_per_thread

        if lines_for_thread == 0 and lines_remain == 0:
            break

        if lines_remain > 0:
            lines_for_thread += 1
            lines_remain -= 1

        t = worker_thread(start_pt, start_pt + lines_for_thread)
        start_pt += lines_for_thread

        t.start()
        threads.append(t)

    for t in threads:
        t.join()

    try:
        outfile.writelines(hosts)
    except IOError as e:
        print(e)
        sys.exit(e.errno)

    sys.exit(0)

if __name__ == '__main__':
    main()
