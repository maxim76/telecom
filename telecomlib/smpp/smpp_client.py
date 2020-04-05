from smpplib.client import Client
import logging
import sys

import smpplib.gsm
import smpplib.client
import smpplib.consts

logging.basicConfig(format='%(asctime)s %(levelname)-8s %(name)-24s %(message)s', datefmt='%Y/%m/%d %H:%M:%S', level='INFO')

class SMPPClient(Client):
    def __init__(self, host, port, systemID, password):
        Client.__init__(self, host, port)
        self.connect()
        self.bind_transceiver(system_id = systemID, password = password)

    def send(self, src, dst, message, isDRRequired):
        srcTon, srcNpi, srcAddr = src.split('.')
        dstTon, dstNpi, dstAddr = dst.split('.')
        parts, encoding_flag, msg_type_flag = smpplib.gsm.make_parts(message)
        logging.info('SMPPClient:send : From: %s.%s.%s To: %s.%s.%s Message:[%s] DR:%d' % (
            srcTon, srcNpi, srcAddr, dstTon, dstNpi, dstAddr, message, isDRRequired))

        for part in parts:
            pdu = self.send_message(
                source_addr_ton = int(srcTon),
                source_addr_npi = int(srcNpi),
                source_addr = srcAddr,
                dest_addr_ton = int(dstTon),
                dest_addr_npi = int(dstNpi),
                dest_addr = dstAddr,
                short_message = part,
                data_coding = encoding_flag,
                esm_class = msg_type_flag,
                regisered_delivery = True
            )


# Unittest
if __name__=="__main__":
    unittestHost = "192.168.1.107"
    unittestPort = 3200
    unittestSystemID = 'test'
    unittestPassword = 'test'
    unittestMessage = u'Test message'
    unittestSrcAddr = '1.1.79161111111'
    unittestDstAddr = '1.1.79161111111'
    client = SMPPClient(unittestHost, unittestPort, unittestSystemID, unittestPassword)
    client.send(unittestSrcAddr, unittestDstAddr, unittestMessage, True)
    client.listen()
