class Transaction:
    """ """

    def __init__(self, sender, recipient, amount):
        self.__sender = sender
        self.__recipient = recipient
        self.__amount = amount

    @property
    def sender(self):
        return self.__sender

    @property
    def recipient(self):
        return self.__recipient

    @property
    def amount(self):
        return self.__amount