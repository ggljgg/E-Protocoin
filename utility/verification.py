from wallet import Wallet
from .hash_util import hash_block, hash_string_256

class Verifier:
    """ """

    @staticmethod
    def valid_proof(transactions, last_hash, proof):
        """ Checks that the proof (nonce) is correctly guessed.

        Arguments:
            :transactions: All open transactions which will be included in the new block.
            :last_hash: The hash of the previous block in the block chain.
            :proof (nonce): A random integer number.
        """
        guess = (str([tx for tx in transactions]) + str(last_hash) + str(proof)).encode()
        return hash_string_256(guess)[0:2] == '00'

    @classmethod
    def verify_chain(cls, blockchain):
        """ Verify the block chain integrity.
        
        Arguments:
            :blockchain: ...
        """
        for (index, block) in enumerate(blockchain):
            if index == 0:
                continue
            if block.previous_hash != hash_block(blockchain[index - 1]):
                return False
            if not cls.valid_proof(block.transactions[:-1],
                            block.previous_hash,
                            block.proof):
                print('Proof of work is invalid!')
                return False
        return True

    @staticmethod
    def verify_transaction(transaction, get_balance, check_funds=True):
        """ Verify a current transaction.

        Arguments:
            :transaction: The transaction that should be verified.
            :get_balance: ...
        """
        if check_funds:
            return get_balance() >= transaction.amount and Wallet.verify_transaction(transaction)
        else:
            return Wallet.verify_transaction(transaction)

    @classmethod
    def verify_transactions(cls, transactions, get_balance):
        """ Verify the all open transactions.
        
        Arguments:
            :transaction: The transaction that should be verified.
            :get_balance: ...
        """
        return all([cls.verify_transaction(tx, get_balance, False) for tx in transactions])  
