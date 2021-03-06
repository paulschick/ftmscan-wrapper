from client import Client


class Tokens(Client):
    def __init__(self, contract_address):
        Client.__init__(self)
        self.url_dict[self.CONTRACT_ADDRESS] = contract_address

    def get_total_supply(self):
        self.url_dict[self.ACTION] = 'tokensupply'
        self.url_dict[self.MODULE] = 'stats'
        self.build_url()
        req = self.connect()
        return req['result']

    def get_token_balance(self, address):
        self.url_dict[self.ADDRESS] = address
        self.url_dict[self.MODULE] = 'account'
        self.url_dict[self.ACTION] = 'tokenbalance'
        self.build_url()
        req = self.connect()
        return req['result']
