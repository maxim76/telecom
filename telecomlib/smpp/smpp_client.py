import logging
import sys
import smpplib.gsm
import smpplib.consts
from smpplib.client import Client


class SMPPClient(Client):
    def __init__(self, host, port, systemID, password):
        Client.__init__(self, host, port)
        self.set_message_sent_handler(self.onSent)
        self.set_message_received_handler(self.onRevc)
        self.connect()
        self.bind_transceiver(system_id = systemID, password = password)

    def onSent(self, pdu, **kwargs):
        logging.info('SMPPClient::onSent sent message seq:%s id:%s' % (str(pdu.sequence), str(pdu.message_id)))

    def onRevc(self, pdu, **kwargs):
        logging.info('SMPPClient::onReceived : received message id: {}\n'.format(pdu.receipted_message_id))


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
                registered_delivery = isDRRequired
            )


# Unittest
if __name__=="__main__":
    logging.basicConfig(format='%(asctime)s %(levelname)-8s %(message)s', datefmt='%Y/%m/%d %H:%M:%S', level='DEBUG')
    logging.info("%s is started in unittest mode" % __file__.split('/')[-1])

    unittestHost = "192.168.1.107"
    unittestPort = 3200
    unittestSystemID = 'test'
    unittestPassword = 'test'
    unittestMessage = u'Test message'
    unittestSrcAddr = '1.1.79161111111'
    unittestDstAddr = '1.1.79162222222'
    client = SMPPClient(unittestHost, unittestPort, unittestSystemID, unittestPassword)
    client.send(unittestSrcAddr, unittestDstAddr, unittestMessage, True)

    from threading import Thread
    t = Thread(target = client.listen)
    t.daemon = True
    t.start()
    import time
    time.sleep(1)

    # TODO: find a proper way of client thread terminating. Now client.disconnect() results in exception
    client.unbind()
    client.disconnect()
    t.join()
