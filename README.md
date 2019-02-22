**本项目fork from https://github.com/lennylxx/ipv6-hosts**

# 源项目不够完善之处

原项目中使用update_hosts.py生成hosts文件，使用方法可见源项目的wiki，或者可以使用`python3 ./update_hosts.py -h`查看help。

源项目做的很好，但是还有一点不完善的地方，我将在以下列举：

- 产生的hosts含有很多注释行，不利于减小hosts文件体积，尤其是对于ROM较小的openwrt来说还是挺大的
- scholar.google.com等一些网站没有AAAA记录，生成hosts是被注释掉的。需要后续手动增加
- 默认是通过ipv6使用google dns查询。这里有两个问题，一个是google dns在大陆已被屏蔽，无法访问；另一个问题就是大陆的ip向google dns请求得到的google ip是台湾彰化机房的。教育网ipv6通往台湾需要绕路香港，会使得速度较慢。
- 默认是udp或者tcp方式查询，但是都是明文传输，无法保证解析结果的可靠性。返回的解析结果有可能是GFW伪造的。
- 返回的ipv6地址可能被GFW屏蔽，导致产生的IPV6 hosts可用性并不是100%。
-感觉源项目有很多ipv4的地址，我觉得没啥必要就去掉了。反正ipv4被屏蔽的也差不多了，修改hosts并没有用。

# 本项目的特性

## ipv6hosts

- 默认使用google dns的api(https://dns.google.com/resolve?)，支持dns over https和edns。其中dns over https保证了解析的可靠性，edns可以确保返回的ip属于香港ip。（貌似同时支持edns和doh的就google一家，不清楚9.9.9.9 opendns支不支持）
- 增加tcp连接检测，提升hosts可用性
- 缓存tcp检测结果，提升运行速度。

## ipv6hostscomment

使用正则表达式写了一个处理脚本ipv6hostscomment.py，并且去掉其他的注释行和ipv4地址，并自动加上需要手动添加的记录（比如scholar.google.com)。主要就是为了缩体积，尽可能减少openwrt rom占用。

windows和UNIX下的换行符不一样，不清楚在作为hosts文件的时候会不会出问题，所以在前面加了一个判断。

# 本项目的使用

## ipv6hosts
```
python3 ipv6hosts.py test -o test_unix -n 5
```
根据test生成test_unix，线程数是5，更多的东西`-h`自行看help。`-c, --cname`无法使用，忘记在help里去掉了 

## ipv6comment
修改一下路径就可以了

# 本项目的缺点
本人懒且水平有限，魔改也就只能改成这样了。ipv6终究不是一个好的办法，说封就可以封的，还是代理更加靠谱，就酱紫
