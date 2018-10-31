import re
iplist={}
addr=r'C:\Users\gyz\Desktop\hosts.out'  # The path of input log file
#addr=r'C:\Users\gyz\Desktop\rawipv6hosts'  # The path of input log file
addr2=r'C:\Users\gyz\Desktop\hosts.out1'
with open(addr2, 'wt') as f: #写入的地址要改
	for raw in open(addr,encoding='UTF-8'):
		if(re.search(r'scholar',raw)):
			gyz=re.match(r'^\#',raw)
			if(not gyz):
				print(raw,end='',file=f)
			else:
				print(re.match(r'^(\#)(.*)',raw).group(2),end='\n',file=f)
		elif((not re.match(r'^\#',raw)) & (not re.search(r'\d{0,3}\.\d{0,3}\.\d{0,3}\.\d{0,3}',raw)) & (not re.match(r'^\s+',raw))):
			print(raw,end='',file=f)
		
  