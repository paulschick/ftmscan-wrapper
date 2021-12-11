from client import Client, EmptyResponse
import re


class Account(Client):
    PAGE_NUM_PATTERN = re.compile(
        r'[1-9](?:\d{0,2})(?:,\d{3})*(?:\.\d*[1-9])?|0?\.\d*[1-9]|0'
    )

    def __init__(self):
        Client.__init__(self)
        self.url_dict[self.MODULE] = 'account'

    def get_balance(self):
        self.url_dict[self.ACTION] = 'balance'
        self.url_dict[self.TAG] = 'latest'
        self.build_url()
        req = self.connect()
        return req['result']

    def get_balance_multiple(self):
        self.url_dict[self.ACTION] = 'balancemulti'
        self.url_dict[self.TAG] = 'latest'
        self.build_url()
        req = self.connect()
        return req['result']

    def get_transaction_page(self, page=1, offset=10000, sort='asc',
                             internal=False, erc20=False) -> list:
        """
        Get a page of transactions, each transaction
        returns list of dict with keys:
            nonce
            hash
            cumulativeGasUsed
            gasUsed
            timeStamp
            blockHash
            value (in wei)
            input
            gas
            isInternalTx
            contractAddress
            confirmations
            gasPrice
            transactionIncex
            to
            from
            isError
            blockNumber
        sort options:
            'asc' -> ascending order
            'desc' -> descending order
        internal options: (currently marked at Beta for etherscan.io)
            True  -> Gets the internal transactions of the address
            False -> (default) get normal external transactions
        erc20 options: (currently marked at Beta for etherscan.io)
            True  -> Gets the erc20 token transcations of the address
            False -> (default) get normal external transactions
        NOTE: not sure if this works for contract addresses, requires testing
        """
        if internal:
            self.url_dict[self.ACTION] = 'txlistinternal'
        elif erc20:
            self.url_dict[self.ACTION] = 'tokentx'
        else:
            self.url_dict[self.ACTION] = 'txlist'
        self.url_dict[self.PAGE] = str(page)
        self.url_dict[self.OFFSET] = str(offset)
        self.url_dict[self.SORT] = sort
        self.build_url()
        req = self.connect()
        return req['result']

    def get_all_transactions(self, offset=9999, sort='asc',
                             internal=False) -> list:
        if internal:
            self.url_dict[self.ACTION] = 'txlistinternal'
        else:
            self.url_dict[self.ACTION] = 'txlist'
        self.url_dict[self.PAGE] = str(1)
        self.url_dict[self.OFFSET] = str(offset)
        self.url_dict[self.SORT] = sort
        self.build_url()
        print(self.url)

        trans_list = []
        while True:
            try:
                self.build_url()
                req = self.connect()
                if "No transactions found" in req['message']:
                    print(
                        "Total number of transactions: {}".format(len(trans_list)))
                    self.page = ''
                    return trans_list
                else:
                    trans_list += req['result']
                    # Find any character block that is a integer of any length
                    page_number = re.findall(Account.PAGE_NUM_PATTERN,
                                             self.url_dict[self.PAGE])
                    print("page {} added".format(page_number[0]))
                    self.url_dict[self.PAGE] = str(int(page_number[0]) + 1)
            except EmptyResponse:
                return trans_list

