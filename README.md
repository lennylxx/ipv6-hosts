利用原项目中的update_hosts.py生成hosts文件


1.含有很多注释行，不利于减小hosts文件体积，对于openwrt来说还是挺大的


2.scholar.google.com没有AAAA记录，生成hosts是被注释掉的。原作者有个merge_snippets.sh没搞懂怎么用，看到里面有`cat snippets/??_*.txt >> $new_hosts_file`的语句，感觉像是把已有的模板追加到一个新文件里面，和sh脚本输入的new_hosts_file没有关系，没有把新的hosts内容融合进去，希望有大神能告诉我怎么回事，在此谢过了。


3.默认是用google的dns查询的，但是很奇怪的是查到的google家的ipv6是台湾的，按理说ipv6香港最快，台湾绕路香港，还要多走一点路。我这里提供的hosts_hk指定香港dns 202.45.84.58查询的。个人用起来好像比台湾的ip快一些。


4.感觉这里面还有好多ipv4的地址，既然叫ipv6 hosts就不该有ipv4，反正我也去掉了。



我用正则表达式写了一个处理脚本ipv6hostscomment.py，能够自动去掉scholar.google.com前面的#，并且去掉其他的注释行和ipv4地址，主要就是为了缩体积，尽可能减少openwrt rom占用。

windows和下的换行符不一样，不清楚在作为hosts文件的时候会不会出问题，所以做了两个版本。默认生成的为换行符为LF的UNIX版本


---------------------------------------------------------------------------------------------
What
----

Hosts file which is used for improving IPv6 access speed to Google, YouTube, 
Facebook, Wikipedia, etc. in Mainland China.

|   \   |                                                                    |
| ----- | ------------------------------------------------------------------ |
| Hosts | https://raw.githubusercontent.com/lennylxx/ipv6-hosts/master/hosts |
| Wiki  | https://github.com/lennylxx/ipv6-hosts/wiki                        |
| Info  | [1e100 servers deployment geoinfo], [SN-domain servers list]       |

* You may need [HTTPS Everywhere] to secure your transmission.
* [How to decode Google SN domains]
* How to [Do It Yourself]

Scripts
-------

[update_hosts.py]

```
usage: update_hosts [OPTIONS] FILE
A simple multi-threading tool used for updating hosts file.

Options:
  -h, --help             show this help message and exit
  -s DNS                 set another dns server, default: 2001:4860:4860::8844
  -o OUT_FILE            output file, default: inputfilename.out
  -t QUERY_TYPE          dig command query type, default: aaaa
  -c, --cname            write canonical name into hosts file
  -n THREAD_NUM          set the number of worker threads, default: 10
```

[merge_snippets.sh]

```
usage: ./merge_snippets.sh new_hosts
```

Some Public DNS Servers
-----------------------

|          |           USA          |           USA          |
| -------- | ---------------------- | ---------------------- |
| Hostname | **ordns.he.net**       | **tserv1.lax1.he.net** |
| IPv6     | 2001:470:20::2         | 2001:470:0:9d::2       | 
| IPv4     | 74.82.42.42            | 66.220.18.42           |
| ISP      | Hurricane Electric Inc.| Hurricane Electric Inc.|
| City     | Anycast                | Los Angeles            |


|          |      Hong Kong         |       Japan        |
| -------- | ---------------------- | ------------------ |
| Hostname | **dns.hutchcity.com**  | **ns01.miinet.jp** |
| IPv4     | 202.45.84.58           | 203.112.2.4        |
| ISP      | Hutchison Whampoa Ltd. | UCOM Corporation   |
| City     | Hong Kong              | Tokyo              |

More public DNS servers please refer to http://public-dns.info

Privacy
-------

* The hosts file just redirects domain to its official IPs. You can check them on any other public DNS servers.
* There is no absolute privacy on the Internet. Learn to protect yourself.
* Act smart.

License
-------

Code of this project is licensed under the [MIT license](LICENSE).  
Content of this project (including hosts files, wiki, and Google sheets) is licensed under [![CC Image]][CC BY-NC-SA 3.0].


[merge_snippets.sh]: merge_snippets.sh
[update_hosts.py]: update_hosts.py
[1e100 servers deployment geoinfo]: https://docs.google.com/spreadsheets/d/1a5HI0lkc1TycJdwJnCVDVd3x6_gemI3CQhNHhdsVmP8
[SN-domain servers list]: https://docs.google.com/spreadsheets/d/14gT1GV1IE0oYCq-1Dy747_5FWNxL26R-9T5htJ485dY
[HTTPS Everywhere]: https://www.eff.org/https-everywhere
[How to decode Google SN domains]: https://github.com/lennylxx/ipv6-hosts/wiki/sn-domains
[Do It Yourself]: https://github.com/lennylxx/ipv6-hosts/wiki/Do-It-Yourself
[CC Image]: https://licensebuttons.net/l/by-nc-sa/3.0/88x31.png
[CC BY-NC-SA 3.0]: https://creativecommons.org/licenses/by-nc-sa/3.0/
