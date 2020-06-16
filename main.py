from flask import Flask, jsonify, request
from wallet import Wallet
from flask_cors import CORS
from blockchain import Blockchain

app = Flask(__name__)
wallet = Wallet()
blockchain = Blockchain(wallet.public_key)

CORS(app)

@app.route('/', methods=['GET'])
def get_user_interface():
    return 'Index page', 200

@app.route('/transactions', methods=['GET'])
def get_open_transactions():
    transactions = blockchain.open_transactions_to_list()
    response = {
        'message': 'The transactions are fetched successfully.',
        'transactions': transactions
    }
    return (jsonify(response), 200)

@app.route('/transaction', methods=['POST'])
def add_transaction():
    if wallet.public_key is None:
        response = {
            'message': 'Creating a transaction failed because the wallet is not set up.',
            'wallet_set_up': not wallet.public_key is None
        }
        return (jsonify(response), 500)

    required_fields = tuple('recipient', 'amount')
    values = request.get_json()

    if not values:
        response = {
            'message': 'No data found.'
        }
        return (jsonify(response), 400)
    if not all([field in values for field in required_fields]):
        response = {
            'message': 'Required data is missing.'
        }
        return (jsonify(response), 400)
    
    recipient = values['recipient']
    amount = values['amount']
    signature = wallet.sign_transaction(recipient, wallet.public_key, amount)
    success = blockchain.add_transaction(recipient, wallet.public_key, amount, signature)

    if success:
        response = {
            'message': 'A transaction is added successfully.',
            'transaction': {
                'sender': wallet.public_key,
                'recipient': recipient,
                'amount': amount,
                'signature': signature
            },
            'funds': blockchain.get_balance()
        }
        return (jsonify(response), 201)
    else:
        response = {
            'message': 'Creating a transaction failed.'
        }
        return (jsonify(response), 500)

@app.route('/balance', methods=['GET'])
def get_balance():
    if wallet.public_key is None:
        response = {
            'message': 'Loading the balance failed because the wallet is not set up.',
            'wallet_set_up': not wallet.public_key is None
        }
        return (jsonify(response), 500)

    response = {
        'message': 'The balance is fetched successfully.',
        'funds': blockchain.get_balance()
    }
    return (jsonify(response), 200)

@app.route('/blockchain', methods=['GET'])
def get_blockchain():
    response = blockchain.to_list()
    return (jsonify(response), 200)

@app.route('/blockchain', methods=['POST'])
def mine():
    if wallet.public_key is None:
        response = {
            'message': 'Creating a block failed because the wallet is not set up.',
            'wallet_set_up': not wallet.public_key is None
        }
        return (jsonify(response), 500)

    block = blockchain.mine_block()
    response = {
        'message': 'A new block is added successfully.',
        'block': block.to_dict(),
        'funds': blockchain.get_balance()
    }
    return (jsonify(response), 201)

@app.route('/wallet', methods=['GET'])
def load_wallet():
    if wallet.load_keys():
        global blockchain
        blockchain = Blockchain(wallet.public_key)
        response = {
            'funds': blockchain.get_balance(),
            'private_key': wallet.private_key,
            'public_key': wallet.public_key
        }
        return (jsonify(response), 201)
    else:
        response = {
            'message': 'Loading the wallet failed...'
        }
        return (jsonify(response), 500)

@app.route('/wallet', methods=['POST'])
def create_wallet():
    wallet.create_keys()

    if wallet.save_keys():
        global blockchain
        blockchain = Blockchain(wallet.public_key)
        response = {
            'funds': blockchain.get_balance(),
            'private key': wallet.private_key,
            'public key': wallet.public_key            
        }
        return (jsonify(response), 201)
    else:
        response = {
            'message': 'Saving the wallet failed...'
        }
        return (jsonify(response), 500)

@app.route('/nodes', methods=['GET'])
def get_nodes():
    response = {
        'all_nodes': blockchain.peer_nodes_to_list()
    }
    return (jsonify(response), 200)

@app.route('/node', methods=['POST'])
def add_node():
    values = request.get_json()

    if not values:
        response = {
            'message': 'No data found.'
        }
        return (jsonify(response), 400)
    if not 'node' in values:
        response = {
            'message': 'No node data found.'
        }
        return (jsonify(response), 400)

    node = values['node']
    blockchain.add_peer_node(node)
    response = {
        'message': 'A new node is added successfully.',
        'all_nodes': blockchain.peer_nodes_to_list()
    }
    return (jsonify(response), 201)

@app.route('/node/<node_url>', methods=['DELETE'])
def remove_node(node_url):
    if (node_url is None) or (node_url == ''):
        response = {
            'message': 'No node data found.'
        }
        return (jsonify(response), 400)

    blockchain.remove_peer_node(node_url)
    response = {
        'message': 'The node is removed successfully.',
        'all_nodes': blockchain.peer_nodes_to_list()
    }
    return (jsonify(response), 200)

if __name__ == '__main__':
    # app.run(host='0.0.0.0', port=5000)
    from node import Node
    node = Node()
    node.listen_for_input()