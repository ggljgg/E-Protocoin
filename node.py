from wallet import Wallet
from blockchain import Blockchain
from utility.verification import Verifier

class Node:
    """ """

    def __init__(self):
        self.__wallet = Wallet()
        self.__blockchain = None

    def listen_for_input(self):
        """ """
        while True:
            print('Please choose:')
            print('1 - Create a new wallet')
            print('2 - Load the wallet')
            print('3 - Show the balance')
            print('4 - Output the blockhain blocks')
            print('5 - Output the open transctions')
            print('6 - Mine a new block')
            print('7 - Add a new transaction')
            print('8 - Check transactions validity')
            print('q - Quit')

            user_choice = self.__get_user_choice()
            if user_choice == '1':
                self.__wallet.create_keys()
                self.__blockchain = Blockchain(self.__wallet.public_key)
                self.__wallet.save_keys()
            elif user_choice == '2':
                self.__wallet.load_keys()
                self.__blockchain = Blockchain(self.__wallet.public_key)
            elif user_choice == '3':
                if self.__wallet.public_key is None:
                    print('Loading the balance failed because the wallet is not set up.')
                    continue
                
                print('Balance of {}: {:6.2f}\n'.format(
                    self.__wallet.public_key,
                    self.__blockchain.get_balance())
                )
            elif user_choice == '4':
                if self.__wallet.public_key is None:
                    print('The wallet is not set up.')
                    continue
                
                self.__print_blockhain_elements()
            elif user_choice == '5':
                if self.__wallet.public_key is None:
                    print('The wallet is not set up.')
                    continue

                self.__print_open_transactions()
            elif user_choice == '6':
                if self.__wallet.public_key is None:
                    print('The wallet is not set up.')
                    continue
                    
                self.__blockchain.mine_block()
            elif user_choice == '7':
                if self.__wallet.public_key is None:
                    print('The wallet is not set up.')
                    continue

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
            elif user_choice == '8':
                if self.__wallet.public_key is None:
                    print('The wallet is not set up.')
                    continue

                if Verifier.verify_transactions(self.__blockchain.open_transactions, self.__blockchain.get_balance):
                    print('\nAll transactions are valid!\n')
                else:
                    print('\nThere are invalid transactions!\n')
            elif user_choice == 'q':
                print('\nThe user left!\n')
                break
            else:
                print('\nThe input was invalid! Please pick a value from the list!\n')
                continue

            if not Verifier.verify_chain(self.__blockchain.chain):
                print('\nInvalid blockchain!\n')
                self.__print_blockhain_elements()
                break

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
        print('{: ^50}'.format('Open transactions'))
        print('-' * 50)
        for tx in self.__blockchain.open_transactions:
            print(tx)
            print('-' * 50)
