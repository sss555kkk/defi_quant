
import requests

from typing import Tuple

class DataCollector:
    def __init__(
        self,
        web3_instance,
        swap_contract_instances:list,
        arbi_intrinsic_gas:int,
        swap_addresses:list,
        swap_function_param_names:dict,
        api_key:str
    ):
        self.w3 = web3_instance
        self.swap_contract_instances = swap_contract_instances
        self.arbi_intrinsic_gas = arbi_intrinsic_gas
        self.swap_addresses = swap_addresses
        self.swap_function_param_names = swap_function_param_names
        self.api_key = api_key

    def get_all_swap_pairs_data(self)->list:
        all_swap_pairs_data = []
        for address in self.swap_addresses:
            one_swap_data = []
            one_swap_data.append(address)
            contract_instance = self.swap_contract_instances[address]
            for i in range(0,2):
                function_to_call = getattr(
                    contract_instance.functions, 
                    self.swap_function_param_names[address][i]['method']
                )
                param = self.swap_function_param_names[address][i]['param']
                result = (
                    function_to_call().call() 
                    if param is None 
                    else function_to_call(param).call()
                )
                one_swap_data.append(result)
            
            all_swap_pairs_data.append(one_swap_data)
            
        return all_swap_pairs_data
    
    def get_intrinsic_gas(self)->int:
        return self.arbi_intrinsic_gas
    
    def get_base_fee_and_priority_fee(self)->Tuple[int,int]:
        url = f'https://api.etherscan.io/api?module=gastracker&action=gasoracle&apikey={self.api_key}'
        response = requests.get(url)
        data = response.json()

        if data['status'] == '1':
            base_fee = data['result']['suggestBaseFee']
            priority_fee = data['result']['ProposeGasPrice']
            
        return base_fee, priority_fee
        
        
        
        
        
        
        
        



        


