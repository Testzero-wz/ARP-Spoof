---
date: 2018-04-06 17:51
status: public
title: ARP
---

# ARP-Spoof
A simple ARP spoof program base on python socket

![](https://github.com/WananpIG/ARP-Spoof/blob/master/_img/17-54-35.jpg)
# Usage
1. Choose a interface first
2. Follow the program and you'll get a functions list
  

![](https://github.com/WananpIG/ARP-Spoof/blob/master/_img/17-57-11.jpg)

Including
+ ARP Scan
+ ARP Spoof
+ Send a custom ARP packet
+ Exit

3\. You can choose one of them

![](https://github.com/WananpIG/ARP-Spoof/blob/master/_img/17-59-19.jpg)

![](https://github.com/WananpIG/ARP-Spoof/blob/master/_img/18-00-09.jpg)

4\. When ARP spoof was succeed, you can attack with driftnet or other tools.

![](https://github.com/WananpIG/ARP-Spoof/blob/master/_img/18-11-23.jpg)
  

(When you want to MITM attack, you should open ipforward first)
``` bash
sudo echo 1 >/proc/sys/net/ipv4/ip_forward
```
5\. You can also send a bunch of custom ARP packets.

![](https://github.com/WananpIG/ARP-Spoof/blob/master/_img/18-17-59.jpg)

**That's it : )**

