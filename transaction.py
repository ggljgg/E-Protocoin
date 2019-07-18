class Transaction:
    """ """
    # __slots__ = ('__sender', '__recepient', '__amount')

    def __init__(self, sender, recepient, amount):
        self.__sender = sender
        self.__recepient = recepient
        self.__amount = amount