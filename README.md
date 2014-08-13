Google Code 上的 [ipv6-hosts](https://code.google.com/p/ipv6-hosts) 项目已经不是很活跃，很多域名已经失效，因此新建一个项目提供有效的ipv6 hosts。

本项目将 ipv6-hosts 地址重新进行分类整理，添加了许多新地址，并且提供了一个刷新地址的脚本。


* **hosts地址:** https://raw.githubusercontent.com/lennylxx/ipv6-hosts/master/hosts  
* **Wiki地址:** https://github.com/lennylxx/ipv6-hosts/wiki
* **<a href="https://docs.google.com/spreadsheets/d/1a5HI0lkc1TycJdwJnCVDVd3x6_gemI3CQhNHhdsVmP8" target="_blank">1e100服务器部署信息表</a>** 

**PS:** 虽然本项目给出了一些域名的IPv6地址，某些网站仍需要使用 HTTPS 协议才能实现穿墙。  
    可以使用 [HTTPS Everywhere](https://www.eff.org/https-everywhere) 插件，支持主流的浏览器。  
    使用 Chrome 的用户也可以在 <code>chrome://net-internals/#hsts</code> 页面加入需要强制使用 HTTPS 访问的域名，并勾选 STS 和 PKP 两个复选框。

====
update_hosts.sh 脚本用法  
<pre>./update_hosts.sh hosts new_hosts</pre>
