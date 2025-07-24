

from solcx import compile_source
from web3 import Web3

def deploy_smart_contract(address:str, address_pk:str):
    """스마트 컨트랙 배포하기"""
    with open('MyTest1.sol', 'r') as file:
        contract_source_code = file.read()

    compiled_sol = compile_source(
        contract_source_code,
        output_values=["abi", "bin"],
        solc_version="0.8.26"
        )

    _, contract_interface = compiled_sol.popitem()
    bytecode = contract_interface['bin']
    abi = contract_interface['abi']

    w3 = Web3(Web3.HTTPProvider("http://127.0.0.1:8545"))
    MyToken = w3.eth.contract(abi=abi, bytecode=bytecode)
    nonce = w3.eth.get_transaction_count(address)
    
    transaction = MyToken.constructor().build_transaction({
        'from': address, 
        'gas': 2_000_000,
        'maxFeePerGas': w3.to_wei(250, 'gwei'),
        'maxPriorityFeePerGas': w3.to_wei(100, 'gwei'),
        'nonce': nonce,
        'chainId': 1337
    })

    signed_txn = w3.eth.account.sign_transaction(
        transaction, 
        private_key=address_pk
    )
    tx_hash = w3.eth.send_raw_transaction(signed_txn.rawTransaction)

    tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
    print(f'Contract deployed at address: {tx_receipt.contractAddress}')




param_addr = '0x5DA49ffdA8C4ede53CaE629E0B019F2039E09511'
param_pk = '0x8a4afcce0c8b6bccc4bd8f6c2290eb69ebfb2602825204a76f6f1629fe174b2c'
param_addr_bytes = bytes.fromhex(param_addr[2:])
param_pk_bytes = bytes.fromhex(param_pk[2:])


deploy_smart_contract(param_addr, param_pk)
