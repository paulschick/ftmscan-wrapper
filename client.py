import os
import json
import requests
import collections
from dotenv import load_dotenv
from pathlib import Path


class ClientException(Exception):
    """Unhandled API client exception"""

    def __init__(self, message=None):
        if message is not None:
            self.message = message

    def __unicode__(self):
        return u'<Err: {0.message}>'.format(self)

    __str__ = __unicode__


class EmptyResponse(ClientException):
    """Empty response from the API"""


class BadRequest(ClientException):
    """Invalid request passed"""


class Client:
    PREFIX = 'https://api.ftmscan.com/api?'
    MODULE = 'module='
    ACTION = '&action='
    CONTRACT_ADDRESS = '&contractaddress='
    ADDRESS = '&address='
    OFFSET = '&offset='
    PAGE = '&page='
    SORT = '&sort='
    BLOCK_TYPE = '&blocktype='
    TO = '&to='
    VALUE = '&value='
    DATA = '&data='
    POSITION = '&position='
    HEX = '&hex='
    GAS_PRICE = '&gasPrice='
    GAS = '&gas='
    START_BLOCK = '&startblock='
    END_BLOCK = '&endblock='
    BLOCKNO = '&blockno='
    TXHASH = '&txhash='
    TAG = '&tag='
    BOOLEAN = '&boolean='
    INDEX = '&index='
    API_KEY = '&apikey='

    def __init__(self, address=None):
        load_dotenv()
        self.config = self._load_config()
        if address is None:
            self.address = self.config['address']
        else:
            self.address = address
        self.api_key = os.getenv('API_KEY')
        self.http = requests.session()
        self.url_dict = collections.OrderedDict([
            (self.MODULE, ''),
            (self.ADDRESS, ''),
            (self.OFFSET, ''),
            (self.PAGE, ''),
            (self.SORT, ''),
            (self.BLOCK_TYPE, ''),
            (self.TO, ''),
            (self.VALUE, ''),
            (self.DATA, ''),
            (self.POSITION, ''),
            (self.HEX, ''),
            (self.GAS_PRICE, ''),
            (self.GAS, ''),
            (self.START_BLOCK, ''),
            (self.END_BLOCK, ''),
            (self.BLOCKNO, ''),
            (self.TXHASH, ''),
            (self.TAG, ''),
            (self.BOOLEAN, ''),
            (self.INDEX, ''),
            (self.API_KEY, self.api_key)])

        # initialize within init
        self.url = None
        self.url_dict[self.ADDRESS] = self.address

    @staticmethod
    def _load_config():
        _path = Path(__file__).parent / 'config.json'
        with open(_path, 'r') as f:
            raw_config = f.read()
            return json.loads(raw_config)

    @staticmethod
    def check_keys_api(data):
        return all(k in data for k in ('jsonrpc', 'id', 'result'))

    def build_url(self):
        self.url = self.PREFIX + ''.join(
            [param + val if val else '' for param, val in
             self.url_dict.items()]
        )

    def connect(self):
        try:
            req = self.http.get(self.url)
        except requests.exceptions.ConnectionError:
            raise ConnectionRefusedError

        if req.status_code == 200:
            if req.text:
                data = req.json()
                status = data.get('status')
                if status == '1' or self.check_keys_api(data):
                    return data
                else:
                    raise EmptyResponse(data.get('message', 'no message'))
        raise BadRequest(
            "Problem with connection, status code: %s" % req.status_code
        )
