import re
iplist={}
addr=r'hosts.out'  # The path of input log file
addr2=r'hosts_hk'
choose=str(input('Windows or Unix or Mac\n'))
if(choose=='Windows'):
	with open(addr2, 'wt',newline='\r\n') as f: #写入的地址要改
		print('127.0.0.1 localhost \n::1 localhost ip6-localhost ip6-loopback',end='\n',file=f)
		for raw in open(addr,encoding='UTF-8'):
			if(re.search(r'scholar',raw)):
				gyz=re.match(r'^\#',raw)
				if(not gyz):
					print(raw,end='',file=f)
				else:
					print(re.match(r'^(\#)(.*)',raw).group(2),end='\n',file=f)
			elif((not re.match(r'^\#',raw)) & (not re.search(r'\d{0,3}\.\d{0,3}\.\d{0,3}\.\d{0,3}',raw)) & (not re.match(r'^\s+',raw)) & (not re.search(r'\.cn',raw))):
				print(raw,end='',file=f)
				
elif(choose=='Unix'):
	with open(addr2, 'wt',newline='\n') as f: #写入的地址要改
		print('127.0.0.1 localhost \n::1 localhost ip6-localhost ip6-loopback',end='\n',file=f)
		for raw in open(addr,encoding='UTF-8'):
			if(re.search(r'scholar',raw)):
				gyz=re.match(r'^\#',raw)
				if(not gyz):
					print(raw,end='',file=f)
				else:
					print(re.match(r'^(\#)(.*)',raw).group(2),end='\n',file=f)
			elif((not re.match(r'^\#',raw)) & (not re.search(r'\d{0,3}\.\d{0,3}\.\d{0,3}\.\d{0,3}',raw)) & (not re.match(r'^\s+',raw)) & (not re.search(r'\.cn',raw))):
				print(raw,end='',file=f)

elif(choose=='Mac'):
	with open(addr2, 'wt',newline='\r') as f: #写入的地址要改
		print('127.0.0.1 localhost \n::1 localhost ip6-localhost ip6-loopback',end='\n',file=f)
		for raw in open(addr,encoding='UTF-8'):
			if(re.search(r'scholar',raw)):
				gyz=re.match(r'^\#',raw)
				if(not gyz):
					print(raw,end='',file=f)
				else:
					print(re.match(r'^(\#)(.*)',raw).group(2),end='\n',file=f)
			elif((not re.match(r'^\#',raw)) & (not re.search(r'\d{0,3}\.\d{0,3}\.\d{0,3}\.\d{0,3}',raw)) & (not re.match(r'^\s+',raw)) & (not re.search(r'\.cn',raw))):
				print(raw,end='',file=f)
else:
	print('Something is wrong! Please input type of OS again')