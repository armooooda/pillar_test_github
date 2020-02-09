import requests, json, logging, time, threading

class SocialNetworkHandler:
    """
    This class handles the SocialNetwork class
    It can tell them to go fetch things they need to
    as well as amalgamate their replies into one to send to server
    """
    def __init__(self):
        self.logger = logging.getLogger('pillar_test.SocialNetworkHandler')

        # these probably should be in an external config file
        self.networks = [   SocialNetwork('https://takehome.io/twitter', 'twitter', 'tweet'),
                            SocialNetwork('https://takehome.io/facebook', 'facebook', 'status'),
                            SocialNetwork('https://takehome.io/instagram', 'instagram', 'picture')]
        self.overall_reply = None
        self.logger.info('initialized with %s networks' %len(self.networks))
        self.gathering_thread = threading.Thread(target=self.gather_reply)
        """
        Here we will launch a thread that constantly gathers information
        from the social networks, so that when we reply to a client, we
        always have the most up to date info & ensure immediate reply
        """
        self.gathering_thread.start()

    def return_reply(self):
        """
        We reply if we have a reply, else we wait
        """
        while True:
            if self.overall_reply is not None:
                return self.overall_reply
            self.logger.info('have no information to give, please wait..')
            time.sleep(0.25)

    def gather_reply(self):
        while True:
            overall_reply = {}
            for n in self.networks:
                overall_reply[n.name] = n.extract_required_response()
            self.logger.info('reply gathered from %s networks' %len(self.networks))
            self.overall_reply = overall_reply
            time.sleep(1)


class SocialNetwork:
    """
    This is a base SocialNetwork class
    it can go gather a response from the predefined http_address
    and amalgamate appropriate required responses
    note: there is minor error catching/handling, wasn't sure exactly how much to put
    i.e. we don't even check the validity of the http address
    """
    def __init__(self, http_address, name, required_response):
        self.logger = logging.getLogger('pillar_test.%s' %name)
        self.name = name
        self.http_address = http_address
        self.response = None
        self.required_response = required_response
        self.logger.info('created instance of SocialNetwork, name: %s, http_address: %s, requred_response: %s' %(self.name, self.http_address, self.required_response))

    def extract_required_response(self):
        self.response = self.get_response()
        self.logger.info('response grabbed successfully, now extracting required response type: %s' %self.required_response)
        try:
            overall_r = []
            for r in self.response:
                overall_r.append(r[self.required_response])
            self.logger.info('gathered %s responses of type %s' %(len(overall_r), self.required_response))

            return overall_r
        except Exception as e:
            """
            This won't happen, but just for fun ¯\_(ツ)_/¯
            """
            self.logger.critical('extraction of required response type: %s FAILED, error: %s' %(self.required_response, e))
            raise ValueError('extraction of required response type: %s FAILED, error: %s' %(self.required_response, e))

    def get_response(self):
        while True:
            self.logger.info('grabbing request from %s' %self.http_address)
            r = requests.get(self.http_address)
            self.logger.info('got request from %s, status: %s' %(self.http_address, r.status_code))
            if r.status_code == 200:
                try:
                    return json.loads(r.text)
                except:
                    self.logger.error ('response from %s is not JSON' %self.http_address)
                break
            else:
                self.logger.error ('status from %s is %s, expected %s' %(self.http_address, r.status_code, 200))