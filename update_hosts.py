#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
import re
import socket
import getopt
import threading
import subprocess
import shlex
import time

blackhole = (
'10::2222',
'101::1234',
'2001::212',
'2001:da8:112::21ae',
'2003:ff:1:2:3:4:5fff:6',
'2003:ff:1:2:3:4:5fff:7',
'2003:ff:1:2:3:4:5fff:8',
'2003:ff:1:2:3:4:5fff:9',
'2003:ff:1:2:3:4:5fff:10',
'2003:ff:1:2:3:4:5fff:11',
'2003:ff:1:2:3:4:5fff:12',
'21:2::2',
'2123::3e12')

dns = {
'google_a':'2001:4860:4860::8888',
'google_b':'2001:4860:4860::8844',
'he_net':'2001:470:20::2',
'lax_he_net':'2001:470:0:9d::2'
}

config = {
'dns':dns['google_b'],
'infile':'hosts',
'outfile':'hosts.new',
'querytype':'aaaa',
'threadnum':10
}

hosts = []
done_num = 0
thread_lock = threading.Lock()

class worker_thread(threading.Thread):
    def __init__(self, start_pt, end_pt):
        threading.Thread.__init__(self)
        self.start_pt = start_pt
        self.end_pt = end_pt
    
    def run(self):
        global hosts, done_num
        for i in range(self.start_pt, self.end_pt):
            line = hosts[i].strip()
            
            with thread_lock:
                done_num += 1

            if line == "" or line[0:2] == '##':
                hosts[i] = line + '\r\n'
                continue

            arr = line.lstrip('#').split()

            if len(arr) == 1:
                domain = arr[0]
            else:
                domain = arr[1]

            flag = False
            if validate_domain(domain):
                ret = query_domain(domain, False)

                if ret in blackhole or not ret:
                    ret = query_domain(domain, True)

                if ret:
                    flag = True
                    arr[0] = ret

            if flag:
                if len(arr) == 1:
                   arr.append(domain)
            else:
                arr[0] = '#' + arr[0]

            hosts[i] = ' '.join(arr)
            hosts[i] += '\r\n'

class watcher_thread(threading.Thread):
    def run(self):
        global hosts, done_num
        total_num = len(hosts)

        wn = int(config['threadnum'])
        if wn > total_num:
            wn = total_num
        print "There are %d threads working..." % wn

        while True:
            with thread_lock:
                dn = done_num

            outbuf = "Total: %d lines, Done: %d lines, Ratio: %d %%.\r"\
                   % (total_num, dn, float(dn)/total_num*100)
            print outbuf,
            sys.stdout.flush()

            if done_num == total_num:
                print outbuf
                break
            time.sleep(1)


def query_domain(domain, tcp):
    cmd = "dig +short +time=2 -6 %s @'%s' '%s'"\
        % (config['querytype'], config['dns'], domain)

    if tcp:
        cmd = cmd[:3] + ' +tcp' + cmd[3:]

    proc = subprocess.Popen(shlex.split(cmd), stdout=subprocess.PIPE)
    out, err = proc.communicate()

    outarr = out.splitlines()

    if len(outarr) == 0:
        ret = ''
    else:
        if validate_ip_addr(outarr[-1]):
            ret = outarr[-1]
        else:
            ret = ''

    return ret

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

def print_help():
    print('''usage: update_hosts [-h] [-s DNS] [-t QUERY_TYPE] [-n THREAD_NUM]
                -i IN_FILE [-o OUT_FILE]
A simple multi-threading tool used to update hosts file.

Options:
  -h, --help             show this help message and exit
  -s DNS                 set another dns server, default: 2001:4860:4860::8844
  -i IN_FILE             input hosts file, default: hosts
  -o OUT_FILE            ouput file, default: hosts.new
  -t QUERY_TYPE          dig command query type, defalut: aaaa
  -n THREAD_NUM          set the number of worker thread, default: 10
''')

def get_config():
    shortopts = 'hs:i:o:t:n:'
    longopts = ['help']

    try:
        optlist, args = getopt.getopt(sys.argv[1:], shortopts, longopts)   
    except getopt.GetoptError as e:
        print e, '\n'
        print_help()
        sys.exit(2)
    
    global config
    for key, value in optlist:
        if key == '-i':
            config['infile'] = value
        elif key == '-s':
            config['dns'] = value
        elif key == '-o':
            config['outfile'] = value
        elif key == '-t':
            config['querytype'] = value
        elif key == '-m':
            config['method'] = value
        elif key == '-n':
            config['threadnum'] = int(value)
        elif key in ('-h', '--help'):
            print_help()
            sys.exit(0)

def main():
    get_config()

    global config, hosts

    try:
        with open(config['infile'], 'r') as infile:
            hosts = infile.readlines()
    except IOError as e:
        print e
        sys.exit(e.errno)

    if os.path.exists(config['outfile']):
        config['outfile'] += '.new'
    
    try:
        outfile = open(config['outfile'], 'w')
    except IOError as e:
        print e
        sys.exit(e.errno)

    threads = []

    t = watcher_thread()
    t.start()
    threads.append(t)

    worker_num = config['threadnum']
    lines_num = len(hosts)

    lines_per_thread = lines_num / worker_num
    lines_remain = lines_num % worker_num

    start_pt = 0

    for i in range(worker_num):
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
        print e
        sys.exit(e.errno)
    
    sys.exit(0)

if __name__ == '__main__':
    main()

