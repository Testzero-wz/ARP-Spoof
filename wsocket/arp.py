import struct
import string
import re


def unpackARP(stream):
    """
    * A 'static' function
    * Parameter stream is recv ARP stream
    * Return a (frameType, opCode, sendMAC, sendIP) tuple
    """
    frameType = struct.unpack_from("B", stream, 12)[0]
    opCode = struct.unpack_from(">H", stream, 20)[0]
    sendMAC = ":".join(
        map(lambda x: hex(x)[2:].zfill(2),
            list(struct.unpack_from("BBBBBB", stream, 22))))
    sendIP = ".".join(
        map(lambda x: str(x), list(struct.unpack_from("BBBB", stream, 28))))
    return (frameType, opCode, sendMAC, sendIP)


class ARP():
    """
    *  A class that packages data into a stream
    """

    def __init__(self, DMAC=None, SMAC=None, SIP=None, DIP=None, **kwargs):

        # ============================== Link package part ==============================

        self.DMAC = "FF:FF:FF:FF:FF:FF" if DMAC is None or DMAC is '' else DMAC
        self.SMAC = "11:22:33:44:55:66" if SMAC is None or SMAC is '' else SMAC

        self.FrameType = kwargs[
            'FrameType'] if 'FrameType' in kwargs else "ARP"

        self.ChechSum = ""  # In ARP packets, we needn't to calculate the CRC check sum

        # ============================== ARP package part ==============================

        self.HardwareType = "\x00\x01"  # EtherNet

        self.ProtocolType = "\x08\x00"  # Ipv4
        """
        * Hardware & Protocol size
        * MAC address length is 6B & IP address length is 4B
        """
        self.H_P_size = "\x06\x04"

        # Default is ARP request and you can switch to ARP reply
        self.ARPType = kwargs['ARPType'] if 'ARPType' in kwargs else "request"

        self.SIP = "192.168.0.2" if SIP is None or SIP is '' else SIP

        self.DIP = "192.168.0.1" if DIP is None or DIP is '' else DIP

        self.stream = ""
        self.__updateStream()

    def __updateStream(self):
        """
        * Update ARP stream
        * Some part of the following is hard-coded of the ARP packet format
        """
        self.stream = self.__mac(self.DMAC) + self.__mac(self.SMAC)

        if self.FrameType == "ARP":

            self.stream += '\x08\x06' + self.HardwareType + self.ProtocolType + self.H_P_size

            if self.ARPType == 'request':
                self.stream += '\x00\x01'
            else:
                self.stream += '\x00\x02'  # reply

            self.stream += self.__mac(self.SMAC) + self.__ip(
                self.SIP) + self.__mac(self.DMAC) + self.__ip(self.DIP)

        self.stream += "\x00" * 18  # padding

    def __mac(self, mac):
        """
        * Calculate host MAC
        """
        stream = ''
        buffer = re.split('[:-]', mac)
        buffer = string.join(buffer, '')
        for i in range(0, len(buffer), 2):
            stream += struct.pack('B', int(buffer[i:i + 2], 16))
        return stream

    def __ip(self, ip):
        """
        * Calculate host IP
        """
        stream = ''
        buffer = re.split('[.]', ip)
        for i in buffer:
            stream += struct.pack('B', int(i))
        return stream
    def getStream(self):
        return self.stream
