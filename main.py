import json, logging, socket, response_server, threading
from social_network import SocialNetworkHandler

"""
here we start all things, i feel like logger comments are pretty explanatory of each action
but i did add comments in modules
"""

logger = logging.getLogger('pillar_test')
logger.setLevel(logging.DEBUG)
fh = logging.FileHandler('pillar_test.log')
fh.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
fh.setFormatter(formatter)
logger.addHandler(fh)

logger.info('starting SocialNetworkHandler..')
snh = SocialNetworkHandler()

logger.info('starting server..')
response_server.server_loop(snh)

