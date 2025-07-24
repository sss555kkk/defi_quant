

import os
from solcx import compile_source

from typing import Tuple


class ContractDepoloyInteractor:
    def __init__(
        self,
        web3,
        network_infos:dict,
        account_private_keys:dict
    ):
        self.w3 = web3
        self.network_infos = network_infos
        self.account_private_keys = account_private_keys
        self.contract_instances = {}
        
    def deploy(
        self,
        from_address:str,
        contract_file_path:str,
        contract_file_name:str,
        *constructor_params:any
    )->str:        
        contract_instance = self.make_web3_contract_instance(
            contract_file_path, 
            contract_file_name
        )
        print (f"contract_instance: {contract_instance}")
        construct_function = self.extract_constructor_in_undeployed_contract(
            contract_instance
        )
        print (f"construct_function: {construct_function}")
        tx_receipt = self.build_transanction_and_send(
            from_address,
            construct_function,
            *constructor_params
        )
        self.save_contract_instance(tx_receipt.contractAddress, contract_instance)
        return tx_receipt.contractAddress
        
    def create_contract_instance(
        self,
        to_address:str,
        contract_file_path:str,
        contract_file_name:str,
    )->None:
        contract_instance = self.make_web3_contract_instance(
            contract_file_path, 
            contract_file_name,
            to_address
        )
        self.save_contract_instance(to_address, contract_instance)

    def call(
        self,
        to_address:str,
        function_name:str,
        *params:any
    )->any:
        function_to_call = self.extract_function_in_deployed_contract(
            function_name, 
            to_address
        )
        result = function_to_call(*params).call()        
        return result

    def transact(
        self,
        from_address:str,
        to_address:str,
        function_name:str,
        *params:any
    )->any:
        function_to_transact = self.extract_function_in_deployed_contract(
            function_name, 
            to_address
        )
        tx_receipt = self.build_transanction_and_send(
            from_address,
            function_to_transact,
            *params
        )
        return tx_receipt
    
    def make_web3_contract_instance(
        self, 
        contract_file_path:str, 
        contract_file_name:str,
        to_address:str=None
    ):
        source_code = self.read_file(contract_file_path, contract_file_name)
        abi, bytecode = self.extract_abi_and_bytecode(source_code)
        contract_instance = self.w3.eth.contract(
            abi=abi, 
            address = to_address,
            bytecode=bytecode
        )
        return contract_instance
    
    def read_file(self, contract_file_path:str, contract_file_name:str)->str:
        full_path = os.path.join(contract_file_path, contract_file_name)
        with open(full_path, 'r') as file:
            contract_source_code = file.read()
        return contract_source_code

    def extract_abi_and_bytecode(self, source_code:str)->Tuple[str,str]:
        compiled_sol = compile_source(
            source_code,
            output_values=["abi", "bin"],
            solc_version="0.8.26"
        )
        _, contract_interface = compiled_sol.popitem()
        abi = contract_interface['abi']
        bytecode = contract_interface['bin']
        return abi, bytecode

    def save_contract_instance(
        self,
        address:str,
        instance
    )->None:
        self.contract_instances[address] = instance
        
    def extract_function_in_deployed_contract(self, function_name:str, to_address:str):
        contract_instance = self.contract_instances[to_address]
        extracted_function = getattr(contract_instance.functions, function_name)
        return extracted_function

    def extract_constructor_in_undeployed_contract(self, contract_instance):
        constructor_function = getattr(contract_instance, 'constructor')
        return constructor_function
    
    def build_transanction_and_send(
        self, 
        from_address:str, 
        extracted_function, 
        *params:any
    ):
        transaction = self.build_transaction(
            from_address, 
            extracted_function, 
            *params
        )
        print (f"transaction: {transaction}")
        signed_tx = self.sign_transaction(
            transaction, 
            self.account_private_keys[from_address]
        )
        print (f"signed_tx: {signed_tx}")
        print ("======")
        print (signed_tx.rawTransaction)
        tx_hash = self.w3.eth.send_raw_transaction(signed_tx.rawTransaction)
        tx_receipt = self.w3.eth.wait_for_transaction_receipt(tx_hash)
        return tx_receipt
    
    def build_transaction(
        self, 
        from_address:str, 
        extracted_function, 
        *params:any
    ):
        transaction = extracted_function(*params).build_transaction({
            'nonce': self.w3.eth.get_transaction_count(from_address),
            'gas': 2_000_000,
            'maxFeePerGas': self.w3.to_wei(250, 'gwei'),
            'maxPriorityFeePerGas': self.w3.to_wei(100, 'gwei'),
            'chainId': self.network_infos['chain_id']
        })
        return transaction
    
    def sign_transaction(self, builded_tx, key:str):
        signed_tx = self.w3.eth.account.sign_transaction(
            builded_tx, 
            private_key=key
        )
        return signed_tx

    def get_my_account_address(self, number:int)->str:
        return list(self.account_private_keys.keys())[number]

    def get_intrinsic_gas(self):
        print ("아직 구현하지 않음")

    def get_account_index(self):
        print ("아직 구현하지 않음")



