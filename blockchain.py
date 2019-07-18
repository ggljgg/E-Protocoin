import functools
import json

from block import Block
from hash_util import hash_block
from transaction import Transaction
from verification import VerificationHelper

MINING_REWARD = 25

class Blockchain:
    """ """

    def __init__(self, hosting_node_id):
        genesis_block = Block(0, '', [], 100)
        self.__chain = [genesis_block]
        self.__open_transactions = []
        self.__hosting_node = hosting_node_id
        self.__load_data()

    @property
    def chain(self):
        return self.__chain[:]

    @chain.setter
    def chain(self, value):
        self.__chain = value

    @property
    def open_transactions(self):
        return self.__open_transactions[:]

# owner = 'Dan'
# participants = {'Dan'}

    def get_last_block(self):
        """ Returns a last block of the current blockchain. """
        if len(self.__chain) == 0:
            return None
        return self.__chain[-1]

    def get_balance(self):
        """ Calculates and returns the participant's balance. """
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

    def proof_of_work(self, last_hash):
        """ Generates a proof of work for open transactions.

        Arguments:
            :last_hash: ...
        """
        proof = 0
        while not VerificationHelper.valid_proof(
            self.__open_transactions,
            last_hash,
            proof
        ):
            proof += 1
        return proof

    def add_transaction(self, recipient, sender, amount=1.0):
        """ Appends a new transaction to the open transaction list and
        transaction participants to the participant set.

        Arguments:
            :sender: The coins sender.
            :recipient: The coins recipient.
            :amount: The coins amount sent with transaction (default = 1.0).
        """
        transaction = Transaction(
            sender,
            recipient,
            amount
        )

        if VerificationHelper.verify_transaction(transaction, self.get_balance):
            self.__open_transactions.append(transaction)
            # participants.add(sender)
            # participants.add(recipient)
            
            # self.__save_data()
            return True
        return False

    def mine_block(self):
        """ Creates a new block for the block chain and
        adds open transactions to it. """
        last_hash = hash_block(self.get_last_block())
        proof = self.proof_of_work(last_hash)

        reward_transaction = Transaction(
            'REWARDING SYSTEM',
            self.__hosting_node,
            MINING_REWARD
        )

        copied_transactions = self.__open_transactions[:]
        copied_transactions.append(reward_transaction)

        block = Block(
            len(self.__chain),
            last_hash,
            copied_transactions,
            proof
        )
        
        self.__chain.append(block)
        self.__open_transactions = []
        # self.__save_data()
        return True

    def __load_data(self):
        """ Initializes a blockhain and open transactions from a file. """
        try:
            with open(file='blockchain.dat', mode='r', encoding='utf-8') as f:
                file_content = f.readlines()
                blockchain = json.loads(file_content[0][:-1])
                open_transactions = json.loads(file_content[1])

                updated_blockchain = []
                for block in blockchain:
                    converted_tx = [Transaction(tx['sender'],
                                                tx['recipient'],
                                                tx['amount'])
                                    for tx in block['transactions']]

                    updated_block = Block(
                        block['index'],
                        block['previous_hash'],
                        converted_tx,
                        block['proof'],
                        block['timestamp']
                    )
                    updated_blockchain.append(updated_block)
                self.chain = updated_blockchain

                updated_transactions = []
                for tx in open_transactions:
                    updated_transaction = Transaction(
                        tx['sender'],
                        tx['recipient'],
                        tx['amount']
                    )
                    updated_transactions.append(updated_transaction)
                self.__open_transactions = updated_transactions
                
        # ################################### 
                print('Data are loaded successfully!')
        except (IOError, IndexError):
            print('Data aren\'t loaded!')
        finally:
            print('Default data are loaded successfully!')

    def __save_data(self):
        """ Saves the current blockhain and open transactions snapshot to a file. """
        try:
            with open(file='blockchain.dat', mode='w', encoding='utf-8') as f:
                saveable_blockchain = [block.__dict__ for block in self.__chain]
                f.write(json.dumps(saveable_blockchain))
                f.write('\n')
                saveable_transactions = [tx.__dict__ for tx in self.__open_transactions]
                f.write(json.dumps(saveable_transactions))
                print('Saving is done successfully!')
        except IOError:
            print('Saving is failed!')
