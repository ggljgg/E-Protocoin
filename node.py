from wallet import Wallet
from blockchain import Blockchain
from utility.verification import VerificationHelper

class Node:
    """ """

    def __init__(self):
        self.__wallet = Wallet()
        self.__blockchain = Blockchain(self.__wallet.public_key)

    def listen_for_input(self):
        """ """
        while True:
            print('Please choose:')
            print('1 - Add a new transaction')
            print('2 - Mine a new block')
            print('3 - Output the blockhain blocks')
            print('4 - Check transactions validity')
            # print('5 - Create a new wallet')
            print('6 - Load wallet')
            print('7 - Save wallet')
            print('q - Quit')

            user_choice = self.__get_user_choice()
            if user_choice == '1':
                tx_data = self.__get_transaction_data()
                recipient, amount = tx_data
                signature = self.__wallet.sign_transaction(
                    recipient,
                    self.__wallet.public_key,
                    amount
                )

                if self.__blockchain.add_transaction(recipient, self.__wallet.public_key, amount, signature):
                    print('\nTransaction is added successful!\n')
                else:
                    print('\nTransaction is failed!\n')

                self.__print_open_transactions()
            elif user_choice == '2':
                if not self.__blockchain.mine_block():
                    print('You don\'t have a wallet!')
            elif user_choice == '3':
                self.__print_blockhain_elements()
            elif user_choice == '4':
                if VerificationHelper.verify_transactions(self.__blockchain.open_transactions, self.__blockchain.get_balance):
                    print('\nAll transactions are valid!\n')
                else:
                    print('\nThere are invalid transactions!\n')
            # elif user_choice == '5':
            #     self.__wallet = Wallet()
            #     self.__blockchain = Blockchain(self.__wallet.public_key)
            elif user_choice == '6':
                self.__wallet.load_keys()
                self.__blockchain = Blockchain(self.__wallet.public_key)
            elif user_choice == '7':
                self.__wallet.save_keys()
            elif user_choice == 'q':
                print('\nThe user left!\n')
                break
            else:
                print('\nThe input was invalid! Please pick a value from the list!\n')
                continue

            if not VerificationHelper.verify_chain(self.__blockchain.chain):
                print('\nInvalid blockchain!\n')
                self.__print_blockhain_elements()
                break

            print('Balance of {}: {:6.2f}\n'.format(
                self.__wallet.public_key,
                self.__blockchain.get_balance())
            )

    def __get_transaction_data(self):
        """ Returns a new transaction data. """
        tx_recipient = input('Enter the transaction recipient: ')
        tx_amount = float(input('Enter your transaction amount: '))
        return (tx_recipient, tx_amount)

    def __get_user_choice(self):
        """ Returns the choice of the user. """
        return input('Your choice: ')

    def __print_blockhain_elements(self):
        """ Output the blockchain list to the console. """
        print('-' * 100)
        for block in self.__blockchain.chain:
            print(block)
            print('-' * 100)

    def __print_open_transactions(self):
        """ """
        print('-' * 50)
        print('{:-^50}'.format('Open transactions'))
        print('-' * 50)
        for tx in self.__blockchain.open_transactions:
            print(tx)
            print('-' * 50)
