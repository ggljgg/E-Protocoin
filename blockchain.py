# Initializing blockchain list
blockchain = []


def get_last_blockchain_value():
    """ Returns the last value of the current blockchain. """
    if len(blockchain) == 0:
        return None
    return blockchain[-1]


def add_transaction(transaction_amount, last_transaction):
    """ Append a new value as well as the last blockchain value to the blockchain.

    Arguments:
        :transaction_amount: The amount that should be added.
        "last_transaction: The last blockchain transaction (default [1]).
    """
    if last_transaction is None:
        last_transaction = [1]
    blockchain.append([last_transaction, transaction_amount])


def get_transaction_value():
    """ Returns a new transaction amount
     as a float. """
    return float(input('Enter your transaction amount please: '))


def get_user_choice():
    """ Returns the choice of the user """
    return input('Your choice: ')


def print_blockhain_elements():
    """ Output the blockchain list to the console """
    for block in blockchain:
        print('Outputting block')
        print(block)

while True:
    print('Please choose:')
    print('1 - Add a new transaction value')
    print('2 - Output the blockhain blocks')
    print('q - Quit')

    user_choice = get_user_choice()
    if user_choice == '1':
        tx_amount = get_transaction_value()
        add_transaction(tx_amount, get_last_blockchain_value())
    elif user_choice == '2':
        print_blockhain_elements()
    elif user_choice == 'q':
        break
    else:
        print('The input was invalid! Please pick a value from the list!')
        continue

    print('The choice is registered!')

print('Done!')
