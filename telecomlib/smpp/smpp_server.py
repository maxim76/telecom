from smpplib.server import Server
import logging


class SMPPServer(Server):

    def __init__(self, port):
        Server.__init__(self, port)
        self.set_authorization_handler(self.custom_authorization_handler)
        self.set_new_sms_handler(self.custom_new_sms_handler)
    
    def custom_authorization_handler(self, pdu, client, **kwargs):
        return True

    def custom_new_sms_handler(self, pdu, client, **kwargs):
        return str(client.next_sequence())


# Unittest
if __name__=="__main__":
    import time
    logging.basicConfig(format='%(asctime)s %(levelname)-8s %(message)s', datefmt='%Y/%m/%d %H:%M:%S', level='DEBUG')
    logging.info("%s is started in unittest mode" % __file__.split('/')[-1])

    unittestPort = 3200
    server = SMPPServer(unittestPort)
    server.up()
    while True:
        time.sleep(1)
