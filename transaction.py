class Transaction:
    """ """

    def __init__(self, sender, recipient, amount, signature):
        self.__sender = sender
        self.__recipient = recipient
        self.__amount = amount
        self.__signature = signature

    def __str__(self):
        return ('sender: {0}\n'
                'recipient: {1}\n'
                'amount: {2}\n'
                'signature: {3}'
                ).format(
                    self.__sender,
                    self.__recipient,
                    self.__amount,
                    self.__signature
                )

    def __repr__(self):
        return str({
            'sender': self.__sender,
            'recipient': self.__recipient,
            'amount': self.__amount,
            'signature': self.__signature
        })

    @property
    def sender(self):
        return self.__sender

    @property
    def recipient(self):
        return self.__recipient

    @property
    def amount(self):
        return self.__amount

    @property
    def signature(self):
        return self.__signature

    def to_dict(self):
        return {
            'sender': self.__sender,
            'recipient': self.__recipient,
            'amount': self.__amount,
            'signature': self.__signature
        }            
