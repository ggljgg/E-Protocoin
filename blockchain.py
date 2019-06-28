import functools
import hashlib
import json

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
    """ Calculates and returns the participant's balance.

    Arguments:
        :participant: The person for whom to calculate the balance.
    """
    tx_sender = [[tx['amount'] for tx in block['transactions'] if tx['sender'] == participant] for block in blockchain]
    open_tx_sender = [tx['amount'] for tx in open_transactions if tx['sender'] == participant]
    tx_sender.append(open_tx_sender)
    amount_sent = functools.reduce(lambda tx_sum, tx_amt: tx_sum + sum(tx_amt) if len(tx_amt) > 0 else tx_sum, tx_sender, 0)

    tx_recipient = [[tx['amount'] for tx in block['transactions'] if tx['recipient'] == participant] for block in blockchain]
    amount_received = functools.reduce(lambda tx_sum, tx_amt: tx_sum + sum(tx_amt) if len(tx_amt) > 0 else tx_sum, tx_recipient, 0)

    return amount_received - amount_sent


def hash_block(block):
    """ Hashes a block and returns a string representation of it.

    Arguments:
        :block: The block that should be hashed.
     """
    return hashlib.sha256(json.dumps(block).encode()).hexdigest()


def add_transaction(recipient, sender=owner, amount=1.0):
    """ Appends a new transaction to the open transaction list and
    transaction participants to the participant set.

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

    if verify_transaction(transaction):
        open_transactions.append(transaction)
        participants.add(sender)
        participants.add(recipient)
        return True

    return False


def mine_block():
    """ Creates a new block for the block chain and
    adds open transactions to it. """
    last_block = blockchain[-1]
    hashed_block = hash_block(last_block)

    reward_transaction = {
        'sender': 'REWARDING SYSTEM',
        'recipient': owner,
        'amount': MINING_REWARD
    }

    copied_transactions = open_transactions[:]
    copied_transactions.append(reward_transaction)

    block = {
        'previous_hash': hashed_block,
        'index': len(blockchain),
        'transactions': copied_transactions
    }
    blockchain.append(block)

    return True


def get_transaction_data():
    """ Returns a new transaction data. """
    tx_recipient = input('Enter the transaction recipient: ')
    tx_amount = float(input('Enter your transaction amount: '))
    return (tx_recipient, tx_amount)


def verify_transaction(transaction):
    """ Verify a current transaction.

    Arguments:
        :transaction: The transaction that should be verified.
    """
    sender_balance = get_balance(transaction['sender'])
    return sender_balance >= transaction['amount']


def verify_chain():
    """ Verify the block chain integrity. """
    for (index, block) in enumerate(blockchain):
        if index == 0:
            continue
        if block['previous_hash'] != hash_block(blockchain[index - 1]):
            return False
    return True


def verify_transactions():
    """ Verify the all open transactions. """
    return all([verify_transaction(tx) for tx in open_transactions])


def get_user_choice():
    """ Returns the choice of the user. """
    return input('Your choice: ')


def print_blockhain_elements():
    """ Output the blockchain list to the console. """
    print('-' * 20)
    for block in blockchain:
        print('Outputting block')
        print(block)
    else:
        print('-' * 20)


waiting_for_input = True
while waiting_for_input:
    print('Please choose:')
    print('1 - Add a new transaction value')
    print('2 - Mine a new block')
    print('3 - Output the blockhain blocks')
    print('4 - Output the participants')
    print('5 - Check transaction validity')
    print('h - Manipulate the chain')
    print('q - Quit')

    user_choice = get_user_choice()
    if user_choice == '1':
        tx_data = get_transaction_data()
        recipient, amount = tx_data
        if add_transaction(recipient, amount=amount):
            print('Transaction is added!')
        else:
            print('Transaction is failed!')
    elif user_choice == '2':
        if mine_block():
            open_transactions = []
    elif user_choice == '3':
        print_blockhain_elements()
    elif user_choice == '4':
        print(participants)
    elif user_choice == '5':
        if verify_transactions():
            print('All transactions are valid.')
        else:
            print('There are invalid transactions!')
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

    print('Balance of {}: {:6.2f}'.format('Dan', get_balance('Dan')))
else:
    print('The user left!')

print('Done!')
