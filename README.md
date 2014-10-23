> Google Code 上的 [ipv6-hosts](https://code.google.com/p/ipv6-hosts) 项目已经不是很活跃，很多域名已经失效，因此新建一个项目提供有效的ipv6 hosts。

简介
----
本项目将 ipv6-hosts 地址重新进行分类整理，添加了许多新地址，并且提供了一个刷新地址的脚本。

| **Hosts:** | https://raw.githubusercontent.com/lennylxx/ipv6-hosts/master/hosts |
|----|----|----|
| **Wiki:** | https://github.com/lennylxx/ipv6-hosts/wiki |
| **Info:** | <a href="https://docs.google.com/spreadsheets/d/1a5HI0lkc1TycJdwJnCVDVd3x6_gemI3CQhNHhdsVmP8" target="_blank">1e100服务器部署信息表</a> |

虽然本项目给出了一些域名的IPv6地址，某些网站仍需要使用 HTTPS 协议才能实现穿墙。  
推荐使用 [HTTPS Everywhere](https://www.eff.org/https-everywhere) 插件，支持主流的浏览器。

> 使用 Chrome 的用户也可以在 <code>chrome://net-internals/#hsts</code> 页面加入需要强制使用 HTTPS 访问的域名，并勾选 STS 和 PKP 两个复选框。

脚本
----
[update_hosts.sh](https://github.com/lennylxx/ipv6-hosts/blob/master/update_hosts.sh) 
> 用于更新 hosts 文件中 IPv6 地址的 BASH 脚本。
> 单线程，速度非常慢。有时间写个多线程的。

<pre>./update_hosts.sh hosts new_hosts</pre>

[merge_snippets.sh](https://github.com/lennylxx/ipv6-hosts/blob/master/merge_snippets.sh) 
> 用于合并 hosts 文件的 BASH 脚本。

<pre>./merge_snippets.sh new_hosts</pre>

常用 IPv6 DNS 服务器
----
* **ordns.he.net**
 * 2001:470:20::2
 * 74.82.42.42
 * 运营商：Hurricane Electric, Inc.
* **google-public-dns-a.google.com**
 * 2001:4860:4860::8888
 * 8.8.8.8
 * 运营商：Google Incorporated
* **google-public-dns-b.google.com**
 * 2001:4860:4860::8844
 * 8.8.4.4
 * 运营商：Google Incorporated
* **ns.ipv6.uni-leipzig.de** （西欧地区适用）
 * 2001:638:902:1::10
 * 139.18.25.34
 * 运营商：University of Leipzig


收录原则
----
1. 本项目主要收集经常访问的且被屏蔽的支持 IPv6 技术的站点，如 Google Search, Gmail, Youtube, Google Plus, Google Docs, Google Play, Wikipedia, Facebook 等等。
2. 暂时不收录不支持 IPv6 且被屏蔽的站点，如 Twitter。
3. 部分收录严重影响上网体验的 IPv4 站点，如 Youtube 部分视频缓存服务器。
4. 不收录支持 IPv6 但不被屏蔽的站点，如教育网内各大高校的网站。
