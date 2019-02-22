import re
iplist={}
addr=r'hosts_hk.out'  # The path of input log file


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

# with open(addr2, 'wt',newline=ss) as f: #写入的地址要改
	# print('127.0.0.1 localhost \n::1 localhost ip6-localhost ip6-loopback',end='\n',file=f)
	# for raw in open(addr,encoding='UTF-8'):
		# if(re.search(r'scholar',raw)):
			# gyz=re.match(r'^\#',raw)
			# if(not gyz):
				# print(raw,end='',file=f)
			# else:
				# print(re.match(r'^(\#)(.*)',raw).group(2),end='\n',file=f)
		# elif((not re.match(r'^\#',raw)) & (not re.search(r'\d{0,3}\.\d{0,3}\.\d{0,3}\.\d{0,3}',raw)) & (not re.match(r'^\s+',raw)) ):
			# print(raw,end='',file=f)
			
with open(addr2, 'wt',newline=ss) as f: #写入的地址要改
	for raw in open(addr,encoding='UTF-8'):
		if((not re.match(r'^\#',raw)) & (not re.search(r'\d{0,3}\.\d{0,3}\.\d{0,3}\.\d{0,3}',raw)) & (not re.match(r'^\s+',raw)) ):
			print(raw,end='',file=f)
	print('127.0.0.1 localhost \n::1 localhost ip6-localhost ip6-loopback \n2404:6800:4005:800::2000 scholar.google.com \n2404:6800:4005:800::2000 scholar.google.com.hk \n2404:6800:4005:800::2000 scholar.google.com.tw \n2404:6800:4005:800::2000 android.clients.google.com \n2404:6800:4005:800::2000 console.developer.google.com\n2404:6800:4008:c06::52 console.developers.google.com\n2404:6800:4008:c06::7b wifi.google.com\n2404:6800:4005:800::2000 www.google.org\n2404:6800:4005:800::2000 www.chromium.org\n2404:6800:4005:800::2000 dev.chromium.org\n2404:6800:4005:800::2000 blog.chromium.org\n2404:6800:4005:800::2000 android.l.google.com\n2404:6800:4005:800::2000 scholar.l.google.com\n2404:6800:4008:c06::7b wifi.l.google.com',end='\n',file=f)
	# if(choose=='Unix'):
# print('2400:da00:2::29 www.baidu.com',end='\n',file=f) #accelerate baidu speed 