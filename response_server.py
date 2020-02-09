import json, logging, socket

def server_loop(social_network_handler):
    """
    this basic server replies to a curl request with SocialNetworkHandler's answer
    """

    logger = logging.getLogger('pillar_test.response_server')

    s = socket.socket()
    host = 'localhost' 
    port = 3000
    s.bind((host, port))
    logger.info('server running on %s:%s' %(host, port))
    s.listen(5)

    while True:
        try:
            c, addr = s.accept()
            logger.info('accepted connection from client %s' %addr[0])

            logger.info('getting necessary information & replying..')
            reply = social_network_handler.return_reply()
            logger.info('will send reply: %s' %json.dumps(reply))

            # so for some reason the below always ends in 
            # curl: (56) Recv failure: Connection reset by peer
            # even though all data is delivered, need to trouble shoot
            c.send(json.dumps(reply).encode())

            logger.info('reply sent, closing connection to %s' %addr[0])    
                    
        except Exception as e:
            logger.error('server loop error: %s' %e)
        
        c.close()
        logger.info('connection to %s closed' %addr[0])
