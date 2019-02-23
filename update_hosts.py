#!/usr/bin/env python3
# -*- coding: utf-8 -*-

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

global ip_unblocked
ip_unblocked=set()

global ip_blocked
ip_blocked=set()



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

            if len(arr) == 1:
                domain = arr[0]
            else:
                domain = arr[1]

            #flag = False
            if validate_domain(domain):
                tcp_flag=ip_available(arr[0])
                if tcp_flag==0 and validate_ip_addr(arr[0]):
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
    ipadlist=('202.40.161.116','202.40.160.109','202.40.160.248','202.40.161.203','123.255.91.97',
    '202.40.161.254','118.140.0.0','124.248.192.1','134.208.0.0','59.125.205.87','140.113.215.224',
    '59.125.39.2','155.69.203.4','61.211.238.90','69.233.219.78')
    #hk,tw,sgp,jp,lax
    nu=len(ipadlist)
    while(counter<nu):
        ipad=ipadlist[counter%nu]    
        url = 'https://dns.google.com/resolve?name=%s&type=%s&edns_client_subnet=%s'%(domain,config['querytype'],ipad)
        '''
        https://github.com/curl/curl/wiki/DNS-over-HTTPS#publicly-available-servers
        import requests
        
        #google dns, edns 
        #QUAD9 dns,
        #cloudflare dns
        
        # url_params = {'name':'www.google.com','type':'aaaa','edns_client_subnet':'175.45.20.138'}
        # url='https://dns.google.com/resolve'
        # url='https://9.9.9.9/dns-query'
        # r = requests.get(url,params = url_params).json()
        # print(r)

    
        # url_params = {'name':'www.google.com','type':'aaaa','edns_client_subnet':'175.45.20.138'}
        # header={'accept': 'application/dns-json'}
        # url='https://cloudflare-dns.com/dns-query'
        # url='https://1.1.1.1/dns-query'
        # r = requests.get(url,params = url_params,headers=header).json()
        # print(r)
                       
        '''
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
                        if ip in ip_unblocked:
                            return ip
                        elif ip in ip_blocked:
                            continue
                        tcp_flag=ip_available(ip)
                        if tcp_flag==0:
                            return ip
                
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
        if tcp_flag ==0:
            ip_unblocked.add(ip)
        else:
            ip_blocked.add(ip)
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
def simplify(hosts,choose=True):
    if(choose):
        addr=config['outfile']  # The path of input file
        ss='\n'
        addr2=addr + 'simplify'          
        with open(addr2, 'wt',newline=ss) as f: #写入的地址要改
            for raw in hosts:
                if((not re.match(r'^\#',raw)) and (not re.search(r'\d{0,3}\.\d{0,3}\.\d{0,3}\.\d{0,3}',raw)) and (not re.match(r'^\s+',raw)) ):
                    print(raw,end='',file=f)
            print('127.0.0.1 localhost \n::1 localhost ip6-localhost ip6-loopback \n2404:6800:4005:800::2000 scholar.google.com \n2404:6800:4005:800::2000 scholar.google.com.hk \n2404:6800:4005:800::2000 scholar.google.com.tw \n2404:6800:4005:800::2000 android.clients.google.com \n2404:6800:4005:800::2000 console.developer.google.com\n2404:6800:4008:c06::52 console.developers.google.com\n2404:6800:4008:c06::7b wifi.google.com\n2404:6800:4005:800::2000 www.google.org\n2404:6800:4005:800::2000 www.chromium.org\n2404:6800:4005:800::2000 dev.chromium.org\n2404:6800:4005:800::2000 blog.chromium.org\n2404:6800:4005:800::2000 android.l.google.com\n2404:6800:4005:800::2000 scholar.l.google.com\n2404:6800:4008:c06::7b wifi.l.google.com',end='\n',file=f)
        
def main():
    get_config()
    
    choose=str(input('Would you want to simplify the hosts(y/n)(Default is yes)\n'))
    if choose=='n':
        choose=False
    else:
        choose=True
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
    simplify(hosts,choose)
    sys.exit(0)

if __name__ == '__main__':
    main()
