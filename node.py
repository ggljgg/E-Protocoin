from uuid import uuid4
from blockchain import Blockchain
from utility.verification import VerificationHelper

class Node:
    """ """

    def __init__(self):
        self.__id = str(uuid4())
        self.__blockchain = Blockchain(self.__id)

    def get_transaction_data(self):
        """ Returns a new transaction data. """
        tx_recipient = input('Enter the transaction recipient: ')
        tx_amount = float(input('Enter your transaction amount: '))
        return (tx_recipient, tx_amount)

    def get_user_choice(self):
        """ Returns the choice of the user. """
        return input('Your choice: ')

    def print_blockhain_elements(self):
        """ Output the blockchain list to the console. """
        print('-' * 25)
        for block in self.__blockchain.chain:
            print(block)
            print('-' * 25)

    def print_open_transactions(self):
        """ """
        print('-' * 23)
        print('{:-^23}'.format('Open transactions'))
        print('-' * 23)
        for tx in self.__blockchain.open_transactions:
            print(tx)
            print('-' * 23)

    def listen_for_input(self):
        """ """
        while True:
            print('Please choose:')
            print('1 - Add a new transaction')
            print('2 - Mine a new block')
            print('3 - Output the blockhain blocks')
            print('4 - Check transactions validity')
            print('q - Quit')

            user_choice = self.get_user_choice()
            if user_choice == '1':
                tx_data = self.get_transaction_data()
                recipient, amount = tx_data

                if self.__blockchain.add_transaction(recipient, self.__id, amount=amount):
                    print('\nTransaction is added successful!\n')
                else:
                    print('\nTransaction is failed!\n')

                self.print_open_transactions()
            elif user_choice == '2':
                self.__blockchain.mine_block()
            elif user_choice == '3':
                self.print_blockhain_elements()
            elif user_choice == '4':
                if VerificationHelper.verify_transactions(self.__blockchain.open_transactions, self.__blockchain.get_balance):
                    print('\nAll transactions are valid.\n')
                else:
                    print('\nThere are invalid transactions!\n')
            elif user_choice == 'q':
                print('\nThe user left!\n')
                break
            else:
                print('\nThe input was invalid! Please pick a value from the list!\n')
                continue

            if not VerificationHelper.verify_chain(self.__blockchain.chain):
                print('\nInvalid blockchain!\n')
                self.print_blockhain_elements()
                break

            print('Balance of {}: {:6.2f}'.format(self.__id, self.__blockchain.get_balance()))
