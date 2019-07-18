from uuid import uuid4
from blockchain import Blockchain
from verification import VerificationHelper

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
        print('-' * 20)
        for block in self.__blockchain.chain:
            print('Outputting block')
            print(block)
        else:
            print('-' * 20)

    def listen_for_input(self):
        """ """
        while True:
            print('Please choose:')
            print('1 - Add a new transaction')
            print('2 - Mine a new block')
            print('3 - Output the blockhain blocks')
            # print('4 - Output the participants')
            print('5 - Check transaction validity')
            print('q - Quit')

            user_choice = self.get_user_choice()
            if user_choice == '1':
                tx_data = self.get_transaction_data()
                recipient, amount = tx_data
                if self.__blockchain.add_transaction(recipient, self.__id, amount=amount):
                    print('Transaction is added!')
                else:
                    print('Transaction is failed!')
                # можно добавить распечатку открытых транзакций
                # print(self.__blockchain.open_transactions)
            elif user_choice == '2':
                self.__blockchain.mine_block()
            elif user_choice == '3':
                self.print_blockhain_elements()
            # elif user_choice == '4':
            #     print(participants)
            elif user_choice == '5':
                if VerificationHelper.verify_transactions(self.__blockchain.open_transactions, self.__blockchain.get_balance):
                    print('All transactions are valid.')
                else:
                    print('There are invalid transactions!')
            elif user_choice == 'q':
                print('The user left!')
                break
            else:
                print('The input was invalid! Please pick a value from the list!')
                continue

            if not VerificationHelper.verify_chain(self.__blockchain.chain):
                print('Invalid blockchain!')
                self.print_blockhain_elements()
                break

            print('Balance of {}: {:6.2f}'.format(self.__id, self.__blockchain.get_balance()))
