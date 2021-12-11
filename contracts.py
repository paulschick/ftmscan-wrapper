from client import Client


class Contract(Client):
    def __init__(self, address):
        Client.__init__(self, address=address)
        self.url_dict[self.MODULE] = 'contract'

    def get_abi(self):
        self.url_dict[self.ACTION] = 'getabi'
        self.build_url()
        req = self.connect()
        return req['result']

    def get_sourcecode(self):
        self.url_dict[self.ACTION] = 'getsourcecode'
        self.build_url()
        req = self.connect()
        return req['result']
