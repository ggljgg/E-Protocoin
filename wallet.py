import binascii
from Crypto import Random
from Crypto.Hash import SHA256
from Crypto.PublicKey import RSA
from Crypto.Signature import PKCS1_v1_5

class Wallet:
    """ """

    def __init__(self):
        self.__private_key = None
        self.__public_key = None

    @property
    def public_key(self):
        return self.__public_key

    @property
    def private_key(self):
        return self.__private_key

    @staticmethod
    def verify_transaction(transaction):
        """ """
        public_key = RSA.importKey(binascii.unhexlify(transaction.sender))
        verifier = PKCS1_v1_5.new(public_key)
        data_hash = SHA256.new(
            (
                str(transaction.recipient) +
                str(transaction.sender) +
                str(transaction.amount)
            ).encode('utf-8')
        )
        return verifier.verify(
            data_hash,
            binascii.unhexlify(transaction.signature)
        )
    
    def create_keys(self):
        """ """
        private_key, public_key = self.__generate_keys()
        self.__private_key = private_key
        self.__public_key = public_key

    def save_keys(self):
        """ """
        if not (self.__public_key is None and self.__private_key is None):
            try:
                with open('wallet.dat', mode='w', encoding='utf-8') as f:
                    f.write(self.__public_key)
                    f.write('\n')
                    f.write(self.__private_key)
                    return True
            except (IOError, IndexError):
                print('Saving the wallet failed...')
                return False

    def load_keys(self):
        """ """
        try:
            with open('wallet.dat', mode='r', encoding='utf-8') as f:
                keys = f.readlines()
                self.__public_key = keys[0][:-1]
                self.__private_key = keys[1]
                return True
        except (IOError, IndexError):
            print('Loading the wallet failed...')
            return False

    def sign_transaction(self, recipient, sender, amount):
        """ """
        signer = PKCS1_v1_5.new(RSA.importKey(binascii.unhexlify(self.__private_key)))
        data_hash = SHA256.new(
            (str(recipient) +
             str(sender) +
             str(amount)
            ).encode('utf-8')
        )

        signature = signer.sign(data_hash)
        return binascii.hexlify(signature).decode('ascii')

    def __generate_keys(self):
        """ """
        private_key = RSA.generate(2048, Random.new().read)
        public_key = private_key.publickey()
        return (
            binascii.hexlify(private_key.exportKey(format='DER')).decode('ascii'),
            binascii.hexlify(public_key.exportKey(format='DER')).decode('ascii')
        )