#!/usr/bin/env python

# Read the wiki for more information
# https://github.com/lennylxx/ipv6-hosts/wiki/sn-domains

import sys
table = '1023456789abcdefghijklmnopqrstuvwxyz'

def iata2sn(iata):
    global table
    sn = ''
    for v in iata:
        if v in table:
            i = ((ord(v) - ord('a')) * 7 + 5) % 36
            sn += table[i]
        else:
            sn += v
    return sn

def sn2iata(sn):
    global table
    iata = ''
    for v in sn:
        if v in table:
            i = table.index(v)
            i = (5 - i % 7) * 5 + i / 7 + 10
            iata += table[i]
        else:
            iata += v
    return iata

def num2code(num):
    global table
    code = ''
    for v in num:
        if v in table:
            i = ((ord(v) - ord('0') + 1) * 7) % 36
            code += table[i]
        else:
            code += v
    return code
    
def code2num(code):
    global table
    num = ''
    for v in code:
        if v in table:
            i = table.index(v)
            i = i / 7 + i % 7 - 1
            num += str(i)
        else:
            num += v
    return num

def main():
    if len(sys.argv) != 3:
        print 'usage:\tconv -i iata\n\tconv -s sn\n\tconv -p isp\n\tconv -g ggc'
        sys.exit(1)

    input = sys.argv[2]
    ret = ''
    if sys.argv[1] == '-i':
        ret += iata2sn(input[0:3])
        ret += num2code(input[3:5])
        ret += 'n'
        ret += num2code(input[6:8])
    elif sys.argv[1] == '-s':
        ret += sn2iata(input[0:3])
        ret += code2num(input[3:5])
        ret += 's'
        ret += code2num(input[6:8])
    elif sys.argv[1] == '-p':
        ret += iata2sn(input[:-1])
        ret += num2code(input[-1])
    elif sys.argv[1] == '-g':
        lst = input.split('-')
        ret += sn2iata(lst[0])
        ret += "-"
        ret += sn2iata(lst[1][0:3])
        ret += code2num(lst[1][3:])
    else:
        print 'Unknown option.'
        sys.exit(1)

    print ret
    sys.exit(0)

if __name__ == '__main__':
    main()
