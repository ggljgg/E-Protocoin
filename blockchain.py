import json
import functools
from block import Block
from transaction import Transaction
from utility.hash_util import hash_block
from utility.verification import Verifier

MINING_REWARD = 25

class Blockchain:
    """ """

    def __init__(self, hosting_node_id):
        genesis_block = Block(0, '', [], 100)
        self.__chain = [genesis_block]
        self.__open_transactions = []
        self.__hosting_node = hosting_node_id
        self.__peer_nodes = set()
        self.__load_data()

    @property
    def chain(self):
        return self.__chain[:]

    @property
    def open_transactions(self):
        return self.__open_transactions[:]

    def to_list(self, blockchain):
        """ """
        return [block.to_dict() for block in blockchain]

    def open_transactions_to_list(self):
        """ """
        return [tx.to_dict() for tx in self.__open_transactions]

    def peer_nodes_to_list(self):
        """ """
        return [node for node in self.__peer_nodes]

    def get_last_block(self):
        """ Returns a last block of the current blockchain. """
        if len(self.__chain) == 0:
            return None
        return self.__chain[-1]

    def get_balance(self):
        """ Calculates and returns the participant's balance. """
        if self.__hosting_node is None:
            return None

        participant = self.__hosting_node

        tx_sender = [[tx.amount
                    for tx in block.transactions
                    if tx.sender == participant]
                    for block in self.__chain]
        open_tx_sender = [tx.amount
                        for tx in self.__open_transactions
                        if tx.sender == participant]
        tx_sender.append(open_tx_sender)
        amount_sent = functools.reduce(lambda tx_sum, tx_amt: tx_sum + sum(tx_amt)
                                    if len(tx_amt) > 0 else tx_sum,
                                    tx_sender, 0)

        tx_recipient = [[tx.amount
                        for tx in block.transactions
                        if tx.recipient == participant]
                        for block in self.__chain]
        amount_received = functools.reduce(lambda tx_sum, tx_amt: tx_sum + sum(tx_amt)
                                        if len(tx_amt) > 0 else tx_sum,
                                        tx_recipient, 0)

        return amount_received - amount_sent

    def add_peer_node(self, node):
        """ """
        self.__peer_nodes.add(node)
        self.__save_data()

    def remove_peer_node(self, node):
        """ """
        self.__peer_nodes.discard(node)
        self.__save_data()

    def add_transaction(self, recipient, sender, amount, signature):
        """ Appends a new transaction to the open transaction list.

        Arguments:
            :sender: The coins sender.
            :recipient: The coins recipient.
            :signature: ...
            :amount: The coins amount sent with transaction.
        """
        if self.__hosting_node is None:
            return None

        transaction = Transaction(
            sender,
            recipient,
            amount,
            signature
        )

        if Verifier.verify_transaction(transaction, self.get_balance):
            self.__open_transactions.append(transaction)
            self.__save_data()
            return True
        return False

    def proof_of_work(self, last_hash):
        """ Generates a proof of work for open transactions.

        Arguments:
            :last_hash: ...
        """
        proof = 0
        while not Verifier.valid_proof(
            self.__open_transactions,
            last_hash,
            proof
        ):
            proof += 1
        return proof

    def mine_block(self):
        """ Creates a new block for the block chain and
        adds open transactions to it. """
        if self.__hosting_node is None:
            return None
        
        last_hash = hash_block(self.get_last_block())
        proof = self.proof_of_work(last_hash)

        reward_transaction = Transaction(
            'REWARDING SYSTEM',
            self.__hosting_node,
            MINING_REWARD,
            ''
        )

        copied_transactions = self.__open_transactions[:]

        if not Verifier.verify_transactions(copied_transactions, self.get_balance):
            return False

        copied_transactions.append(reward_transaction)

        block = Block(
            len(self.__chain),
            last_hash,
            copied_transactions,
            proof
        )
        
        self.__chain.append(block)
        self.__open_transactions = []
        self.__save_data()
        return block

    def __load_data(self):
        """ Initializes a blockhain and open transactions from a file. """
        try:
            with open(file='blockchain.dat', mode='r', encoding='utf-8') as f:
                file_content = f.readlines()

                blockchain = json.loads(file_content[0][:-1])
                open_transactions = json.loads(file_content[1][:-1])
                peer_nodes = json.loads(file_content[2][:-1])

                self.__chain = self.__loadable_blockchain(blockchain)
                self.__open_transactions = self.__loadable_transactions(open_transactions)
                self.__peer_nodes = self.__loadable_peer_nodes(peer_nodes)

            print('\nData are loaded from source successfully!\n')
        except (IOError, IndexError):
            print(
                '\nData aren\'t loaded from source!\n'
                'Default data are loaded successfully!\n'
            )

    def __save_data(self):
        """ Saves the current blockhain and open transactions snapshot to a file. """
        prepared_data = (
            self.to_list(self.__chain),
            self.open_transactions_to_list(),
            self.peer_nodes_to_list()
        )
        
        try:
            with open(file='blockchain.dat', mode='w', encoding='utf-8') as f:
                for data in prepared_data:
                    f.write(json.dumps(data))
                    f.write('\n')
            print('\nSaving is done successfully!\n')
        except IOError:
            print('\nSaving is failed!\n')

    def __loadable_transaction(self, transaction):
        """ """
        return Transaction(
            transaction['sender'],
            transaction['recipient'],
            transaction['amount'],
            transaction['signature']
        )

    def __loadable_transactions(self, transactions):
        """ """
        return [
            self.__loadable_transaction(tx)
            for tx in transactions
        ]

    def __loadable_block(self, block):
        """ """
        return Block(
            block['index'],
            block['previous hash'],
            self.__loadable_transactions(block['transactions']),
            block['proof'],
            block['timestamp']
        )

    def __loadable_blockchain(self, blockchain):
        """ """
        return [
            self.__loadable_block(block)
            for block in blockchain
        ]

    def __loadable_peer_nodes(self, peer_nodes):
        """ """
        return {peer_node for peer_node in peer_nodes}
