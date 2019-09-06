class Transaction:
    """ """

    def __init__(self, sender, recipient, amount):
        self.__sender = sender
        self.__recipient = recipient
        self.__amount = amount

    def __str__(self):
        return ('sender: {0}\n'
                'recipient: {1}\n'
                'amount: {2}'
                ).format(
                    self.__sender,
                    self.__recipient,
                    self.__amount
                )

    def __repr__(self):
        return str({
            'sender': self.__sender,
            'recipient': self.__recipient,
            'amount': self.__amount
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

    def to_dict(self):
        return {
            'sender': self.__sender,
            'recipient': self.__recipient,
            'amount': self.__amount
        }            
