+++
author = ""
comments = false
date = "2017-01-01T15:53:14-05:00"
draft = false
image = "img/sorting-hat.jpg"
menu = ""
share = true
slug = "post-title"
title = "Sorting IPs"

+++

I scan my home network frequently. There are a good number of smarthome devices, raspberry pies, phones,
laptops, PCs etc. Using nmap to quickly scan a network is too slow for me - and it is a challenge to
parse the output for easy reading (of course I would use awk to do that). So I use arp-scan (available
in most repositories). So output might look like this:

```
$ sudo arp-scan -I wlo1 192.168.1.0/24
Interface: wlo1, datalink type: EN10MB (Ethernet)
Starting arp-scan 1.8.1 with 256 hosts (http://www.nta-monitor.com/tools/arp-scan/)
192.168.1.1     44:94:fc:93:4f:26       (Unknown)
192.168.1.2     00:17:88:2a:b5:12       Philips Lighting BV
192.168.1.17    b8:27:eb:42:e9:01       (Unknown)
192.168.1.62    b8:27:eb:42:e9:01       (Unknown)
192.168.1.72    b8:27:eb:42:e9:01       (Unknown)

<!--more-->

192.168.1.4     50:f5:da:52:08:8b       (Unknown)
192.168.1.90    54:42:49:a4:d7:b0       Sony Corporation
192.168.1.11    64:eb:8c:6f:e7:4c       (Unknown)
192.168.1.13    5c:ff:35:21:21:d4       Wistron Corporation
192.168.1.8     7c:c7:09:88:07:79       (Unknown)
192.168.1.17    c8:3a:35:cb:90:8f       Tenda Technology Co., Ltd. (DUP: 2)
192.168.1.10    c0:c1:c0:dc:29:69       Cisco-Linksys, LLC
192.168.1.7     6c:ad:f8:33:09:e8       (Unknown)
192.168.1.21    f0:25:b7:35:e7:33       (Unknown)
192.168.1.29    c0:c1:c0:dc:29:69       Cisco-Linksys, LLC
192.168.1.61    b8:27:eb:4b:b6:4c       (Unknown)
192.168.1.76    1c:3e:84:5e:b5:bc       (Unknown)
192.168.1.64    c0:c1:c0:dc:29:69       Cisco-Linksys, LLC
192.168.1.62    c8:3a:35:cb:90:8f       Tenda Technology Co., Ltd. (DUP: 2)
192.168.1.72    c8:3a:35:cb:90:8f       Tenda Technology Co., Ltd. (DUP: 2)
192.168.1.20    b2:c5:54:0b:de:50       (Unknown)
192.168.1.24    00:0d:4b:80:18:6d       Roku, LLC
192.168.1.131   50:c7:bf:13:44:73       (Unknown)

23 packets received by filter, 0 packets dropped by kernel
Ending arp-scan 1.8.1: 256 hosts scanned in 1.576 seconds (162.44 hosts/sec). 23 responded

```

But this listing is unsorted; I need it in ascending IP order. The solution is to creatively
use the unix sort command declaring the field "termination" character as "." and then declaring
the key fields to sort on. Here is the final run:

```
$ sudo arp-scan -I wlo1 192.168.1.0/24|sort -t . -k3,3n -k4,4n

24 packets received by filter, 0 packets dropped by kernel
Interface: wlo1, datalink type: EN10MB (Ethernet)
Starting arp-scan 1.8.1 with 256 hosts (http://www.nta-monitor.com/tools/arp-scan/)
192.168.1.1     44:94:fc:93:4f:26       (Unknown)
192.168.1.2     00:17:88:2a:b5:12       Philips Lighting BV
192.168.1.4     50:f5:da:52:08:8b       (Unknown)
192.168.1.7     6c:ad:f8:33:09:e8       (Unknown)
192.168.1.8     7c:c7:09:88:07:79       (Unknown)
192.168.1.10    c0:c1:c0:dc:29:69       Cisco-Linksys, LLC
192.168.1.11    64:eb:8c:6f:e7:4c       (Unknown)
192.168.1.13    5c:ff:35:21:21:d4       Wistron Corporation
192.168.1.17    b8:27:eb:42:e9:01       (Unknown)
192.168.1.17    c8:3a:35:cb:90:8f       Tenda Technology Co., Ltd. (DUP: 2)
192.168.1.20    b2:c5:54:0b:de:50       (Unknown)
192.168.1.21    f0:25:b7:35:e7:33       (Unknown)
192.168.1.24    00:0d:4b:80:18:6d       Roku, LLC
192.168.1.29    c0:c1:c0:dc:29:69       Cisco-Linksys, LLC
192.168.1.61    b8:27:eb:4b:b6:4c       (Unknown)
192.168.1.62    b8:27:eb:42:e9:01       (Unknown)
192.168.1.62    c8:3a:35:cb:90:8f       Tenda Technology Co., Ltd. (DUP: 2)
192.168.1.63    b2:c5:54:0b:de:50       (Unknown)
192.168.1.64    c0:c1:c0:dc:29:69       Cisco-Linksys, LLC
192.168.1.72    b8:27:eb:42:e9:01       (Unknown)
192.168.1.72    c8:3a:35:cb:90:8f       Tenda Technology Co., Ltd. (DUP: 2)
192.168.1.76    1c:3e:84:5e:b5:bc       (Unknown)
192.168.1.90    54:42:49:a4:d7:b0       Sony Corporation
192.168.1.131   50:c7:bf:13:44:73       (Unknown)
Ending arp-scan 1.8.1: 256 hosts scanned in 1.520 seconds (168.42 hosts/sec). 24 responded
```

Enjoy
-g-
