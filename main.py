
from flask import Flask, render_template, request

from web3 import Web3

infura_url = "https://goerli.infura.io/v3/35193e681cf24bdd8a422b3422fed8fc"
host_account = "0xa2dd577e83AE3E55867De23DaCc645eF9a94B1Cd"
contract_address = '0x67637c46043A62C2277eEb1894Be7d684334Ffe4'
web3 = Web3(Web3.HTTPProvider(infura_url))




app = Flask(__name__)

@app.route('/', methods =['GET', 'POST'])
def main():
    if request.method=='POST':
        from_account = str(request.form['account'])
        private_key = str(request.form['pkey'])

        address_from = web3.toChecksumAddress(from_account)
        address_to = web3.toChecksumAddress(contract_address)

        nonce = web3.eth.getTransactionCount(address_from)
        amount = request.form['amount']
        tx = {
            'nonce': nonce,
            'to' : address_to,
            'value': web3.toWei(str(amount),'ether'),
            'gas': 125000, #min gas
            'gasPrice': web3.toWei(40,'gwei')
        }

        signed_tx = web3.eth.account.sign_transaction(tx,private_key)
        tx_transaction = web3.eth.sendRawTransaction(signed_tx.rawTransaction)
        return render_template('exit.html')
    else:
        return render_template('home.html')


if __name__ == "__main__":
    app.run(debug=False, host='0.0.0.0', port=3023)

