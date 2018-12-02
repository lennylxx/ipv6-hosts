import re
iplist={}
addr=r'hosts.out'  # https://raw.githubusercontent.com/sharuijinfriend/ipv6-hosts/master/hosts.out
addr1=r'hosts' #https://raw.githubusercontent.com/lennylxx/ipv6-hosts/master/hosts
# Google hk CERNET2-> HKIX. So using HK dns is better
# Wikipedia hk CERNET2->HE US_WEST->HE TOKYO->HK. So using US dns will be better.
conti=1
wikitrue=0
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

			
with open(addr2, 'wt',newline=ss) as f: 
	for raw in open(addr,encoding='UTF-8'):#google,facebook,instagram
		if(not wikitrue):
			wikitrue=re.search(r'(?i)wiki',raw)
		if(not wikitrue):
			if((not re.match(r'^\#',raw)) & (not re.search(r'\d{0,3}\.\d{0,3}\.\d{0,3}\.\d{0,3}',raw)) & (not re.match(r'^\s+',raw)) ):
				print(raw,end='',file=f)
	wikitrue=0
	appletrue=0
	for raw in open(addr1,encoding='UTF-8'):
		if(not wikitrue):
			wikitrue=re.search(r'(?i)wiki',raw)
		if(wikitrue):
			appletrue=re.search(r'(?i)apple',raw)
		if(bool(wikitrue) & (not appletrue)):
			if((not re.match(r'^\#',raw)) & (not re.search(r'\d{0,3}\.\d{0,3}\.\d{0,3}\.\d{0,3}',raw)) & (not re.match(r'^\s+',raw)) ):
				print(raw,end='',file=f)
	print('127.0.0.1 localhost \n::1 localhost ip6-localhost ip6-loopback \n2404:6800:4005:800::2000 scholar.google.com \n2404:6800:4005:800::2003 scholar.google.com.hk \n2404:6800:4005:800::2003 scholar.google.com.tw \n2404:6800:4005:800::2000 android.clients.google.com \n2404:6800:4005:800::2000 console.developer.google.com\n2404:6800:4008:c06::52 console.developers.google.com\n2404:6800:4008:c06::7b wifi.google.com\n2404:6800:4005:800::2000 www.google.org\n2404:6800:4005:800::2000 www.chromium.org\n2404:6800:4005:800::2000 dev.chromium.org\n2404:6800:4005:800::2000 blog.chromium.org\n2404:6800:4005:800::2000 android.l.google.com\n2404:6800:4005:800::2000 scholar.l.google.com\n2404:6800:4008:c06::7b wifi.l.google.com',end='\n',file=f)
	if(choose=='Unix'):
		print('2400:da00:2::29 www.baidu.com',end='\n',file=f) #accelerate baidu speed in qujiang
		
