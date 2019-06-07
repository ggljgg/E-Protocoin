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
        last_transaction = [1.0]
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
    print('-' * 20)
    for block in blockchain:
        print('Outputting block')
        print(block)
    else:
        print('-' * 20)


def verify_chain():
    """ Checks the block chain integrity """
    is_valid = True
    for block_index in range(len(blockchain)):
        if block_index == 0:
            continue
        elif blockchain[block_index][0] == blockchain[block_index - 1]:
            is_valid = True
        else:
            is_valid = False
            break
    return is_valid

waiting_for_input = True
while waiting_for_input:
    print('Please choose:')
    print('1 - Add a new transaction value')
    print('2 - Output the blockhain blocks')
    print('h - Manipulate the chain')
    print('q - Quit')

    user_choice = get_user_choice()
    if user_choice == '1':
        tx_amount = get_transaction_value()
        add_transaction(tx_amount, get_last_blockchain_value())
    elif user_choice == '2':
        print_blockhain_elements()
    elif user_choice == 'h':
        if len(blockchain) >= 1:
            blockchain[0] = [2]
    elif user_choice == 'q':
        # break
        waiting_for_input = False
    else:
        print('The input was invalid! Please pick a value from the list!')
        continue

    if not verify_chain():
        print('Invalid blockchain')
        break
else:
    print('Done!')
