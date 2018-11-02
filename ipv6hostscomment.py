import re
iplist={}
addr=r'hosts.out'  # The path of input log file


conti=1
while(conti):
	choose=str(input('Windows or Unix or Mac\n'))
	if(choose=='Windows'):
		ss='\r\n'
		addr2=r'hosts_hk_win'
		conti=0
	elif(choose=='Unix'):
		ss='\n'
		addr2=r'hosts_hk_unix'
		conti=0
	elif(choose=='Mac'):
		ss='\r'
		addr2=r'hosts_hk_mac'
		conti=0
	else:
		print('Something is wrong! Please input type of OS again')

with open(addr2, 'wt',newline=ss) as f: #写入的地址要改
	print('127.0.0.1 localhost \n::1 localhost ip6-localhost ip6-loopback',end='\n',file=f)
	for raw in open(addr,encoding='UTF-8'):
		if(re.search(r'scholar',raw)):
			gyz=re.match(r'^\#',raw)
			if(not gyz):
				print(raw,end='',file=f)
			else:
				print(re.match(r'^(\#)(.*)',raw).group(2),end='\n',file=f)
		elif((not re.match(r'^\#',raw)) & (not re.search(r'\d{0,3}\.\d{0,3}\.\d{0,3}\.\d{0,3}',raw)) & (not re.match(r'^\s+',raw)) ):
			print(raw,end='',file=f)