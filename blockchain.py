MINING_REWARD = 25

genesis_block = {
    'previous_hash': '',
    'index': 0,
    'transactions': []
}

blockchain = [genesis_block]
open_transactions = []
owner = 'Dan'
participants = {'Dan'}


def get_last_blockchain_value():
    """ Returns the last value of the current blockchain. """
    if len(blockchain) == 0:
        return None
    return blockchain[-1]


def get_balance(participant):
    """  """
    tx_sender = [[tx['amount'] for tx in block['transactions'] if tx['sender'] == participant] for block in blockchain]
    amount_sent = 0
    for tx in tx_sender:
        if len(tx) > 0:
            amount_sent += tx[0]

    tx_recipient = [[tx['amount'] for tx in block['transactions'] if tx['recipient'] == participant] for block in blockchain]
    amount_received = 0
    for tx in tx_recipient:
        if len(tx) > 0:
            amount_received += tx[0]

    return amount_received - amount_sent


def hash_block(block):
    """  """
    return '-'.join([str(block[key]) for key in block])


def add_transaction(recipient, sender=owner, amount=1.0):
    """ Append a new value as well as the last blockchain value to the blockchain.

    Arguments:
        :sender: The coins sender.
        :recipient: The coins recipient.
        :amount: The coins amount sent with transaction (default = 1.0).
    """
    transaction = {
        'sender': sender,
        'recipient': recipient,
        'amount': amount
    }

    open_transactions.append(transaction)
    participants.add(sender)
    participants.add(recipient)


def mine_block():
    """  """
    last_block = blockchain[-1]
    hashed_block = hash_block(last_block)

    reward_transaction = {
        'sender': 'REWARDING SYSTEM',
        'recipient': owner,
        'amount': MINING_REWARD
    }
    open_transactions.append(reward_transaction)

    block = {
        'previous_hash': hashed_block,
        'index': len(blockchain),
        'transactions': open_transactions
    }
    blockchain.append(block)

    return True


def get_transaction_data():
    """ Returns a new transaction data. """
    tx_recipient = input('Enter the transaction recipient: ')
    tx_amount = float(input('Enter your transaction amount: '))
    return (tx_recipient, tx_amount)


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
    """ Verify the block chain integrity """
    for (index, block) in enumerate(blockchain):
        if index == 0:
            continue
        if block['previous_hash'] != hash_block(blockchain[index - 1]):
            return False
    return True

waiting_for_input = True
while waiting_for_input:
    print('Please choose:')
    print('1 - Add a new transaction value')
    print('2 - Mine a new block')
    print('3 - Output the blockhain blocks')
    print('4 - Output the participants')
    print('h - Manipulate the chain')
    print('q - Quit')

    user_choice = get_user_choice()
    if user_choice == '1':
        tx_data = get_transaction_data()
        recipient, amount = tx_data
        add_transaction(recipient, amount=amount)
    elif user_choice == '2':
        if mine_block():
            open_transactions = []
    elif user_choice == '3':
        print_blockhain_elements()
    elif user_choice == '4':
        print(participants)
    elif user_choice == 'h':
        if len(blockchain) >= 1:
            blockchain[0] = {
                'previous_hash': '',
                'index': 0,
                'transactions': [{
                    'sender': 'sender',
                    'recipient': 'recipient',
                    'amount': 1000
                }]
            }
    elif user_choice == 'q':
        waiting_for_input = False
    else:
        print('The input was invalid! Please pick a value from the list!')
        continue

    if not verify_chain():
        print('Invalid blockchain!')
        print_blockhain_elements()
        break

    print(get_balance('Dan'))
else:
    print('The user left!')

print('Done!')
