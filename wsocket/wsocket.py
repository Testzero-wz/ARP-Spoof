import socket
import psutil
from struct import *
import arp, sys

"""
* Some protocol type in link layer (The field of FrameType )
"""
ETH_TYPE_PUP = 0x0200  # PUP protocol
ETH_TYPE_IP = 0x0800  # IP protocol
ETH_TYPE_ARP = 0x0806  # address resolution protocol
ETH_TYPE_AOE = 0x88a2  # AoE protocol
ETH_TYPE_CDP = 0x2000  # Cisco Discovery Protocol
ETH_TYPE_DTP = 0x2004  # Cisco Dynamic Trunking Protocol
ETH_TYPE_REVARP = 0x8035  # reverse addr resolution protocol
ETH_TYPE_8021Q = 0x8100  # IEEE 802.1Q VLAN tagging
ETH_TYPE_IPX = 0x8137  # Internetwork Packet Exchange
ETH_TYPE_IP6 = 0x86DD  # IPv6 protocol
ETH_TYPE_PPP = 0x880B  # PPP
ETH_TYPE_MPLS = 0x8847  # MPLS
ETH_TYPE_MPLS_MCAST = 0x8848  # MPLS Multicast
ETH_TYPE_PPPoE_DISC = 0x8863  # PPP Over Ethernet Discovery Stage
ETH_TYPE_PPPoE = 0x8864  # PPP Over Ethernet Session Stage
ETH_TYPE_LLDP = 0x88CC  # Link Layer Discovery Protocol
ETH_TYPE_TEB = 0x6558  # Transparent Ethernet Bridging


class wsocket:
    """
    * Likely inherit socket class
    * But I'm choice composition rather than inheritance
    * I don't need so many method or function
    """
    # Error Type
    valueError = "Invalid Value"
    typeError = "Type Error"
    dependencyError = "Dependency Error"

    def __init__(self):
        """
        * Initial a raw socket and set receive buffer size
        """
        self.socket = socket.socket(socket.AF_PACKET, socket.SOCK_RAW)
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_RCVBUF, 256)
        self.interFaceList = self.__scanInterface()
        self.interFace = None
        self.subnetSize = None
        self.ip_block = None
        self.host = None
        self.MAC = None
        self.defaultGateWay = None

    def settimeout(self, time=5):
        self.socket.settimeout(time)

    def send(self, stream, **kwargs):
        """
        * Makes send function can accept our ARP class
        """
        if isinstance(stream, arp.ARP):
            self.socket.send(stream.getStream(), **kwargs)
        elif isinstance(stream, str):
            self.socket.send(stream, **kwargs)
        else:
            self.raiseError(
                self.typeError,
                "The data you want to send must a string or ARP type! ")

    def recv(self, size=1024):
        return self.socket.recv(size)

    def bind(self, interFace):
        if isinstance(interFace, tuple) == False:
            self.raiseError(self.typeError,
                            "InterFace parameter must be a tuple!")
        else:
            self.socket.bind(interFace)

    def setInterFace(self, interface):
        """
        * Setting up the adapter which we use to send the ARP packets.
        """
        if isinstance(interface, tuple):
            self.interFace = interface

        elif isinstance(interface, int):
            """
            * Select a adapter from our interFaceList. 
            """
            try:
                self.interFace = self.interFaceList[interface]
            except:
                self.raiseError(self.valueError,
                                "The index you given is out of range")
        else:
            self.raiseError(
                self.typeError,
                "The interFace you want to select must be an interface tuple or an int index"
            )
            return 0
        # Calculate network number
        self.ip_block = map(lambda (x, y): int(x) & int(y),
                            zip(self.interFace[1].split('.'),
                                self.interFace[2].split('.')))
        # Set a default gateway
        GateWay = self.ip_block[:]
        GateWay[-1] = GateWay[-1] + 1
        self.defaultGateWay = ".".join(map(lambda x: str(x), GateWay))

        # Calculate subnet size
        subnetSize = 0
        for i in map(lambda x: int(x), self.interFace[2].split('.')):
            t = 255 - i
            subnetSize = subnetSize << 8
            subnetSize += t
        self.subnetSize = subnetSize
        self.host = self.interFace[1]
        self.MAC = self.interFace[3]
        return 1

    def __scanInterface(self):
        """
        * use psutil to get net interface info
        * return inferFaceList
        """

        inferFaceList = []
        info = psutil.net_if_addrs()
        """
        *  return a dictionary like
        *  {interfaceName: [class psutil._common.snic(ipv4),class psutil._common.snic(ipv6),class psutil._common.snic(ether)]}
        *  The class psutil._common.snic is override the operator [] and you can fetch it's value via [index]
        *  Actually, psutil._common.snic is a tuple
        *  e.g.
        *  psutil._common.snic(  family=2, 
        *                        address='192.168.1.34', 
        *                        netmask='255.255.255.0',
        *                        broadcast='192.168.242.255',
        *                        ptp=None)
        """
        for interName, snicList in info.items():
            for snic in snicList:
                """
                * if family == 2  (I guess it's etherNet family) and
                * address !== '127.0.0.1' (We don't need Loopback Adapter )
                """
                if snic[0] == 2 and not snic[1] == '127.0.0.1':
                    inferFaceList.append((interName, snic[1], snic[2],
                                          snicList[2][1]))
        return inferFaceList

    def raiseError(self, errorType, message, exitFlag=0):
        print "[!]", "****", errorType, "****"
        print message
        if exitFlag:
            exit()
