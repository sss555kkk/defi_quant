

from flash_swap.data_collector import (
    DataCollector
)
from flash_swap.arbi_transact_creator import (
    ArbiTransactCreator
)
from flash_swap.converter import (
    Converter
)
from flash_swap.presenter import (
    Presenter
)
from flash_swap.controller import (
    Controller
)

from flash_swap.setting_info import (
    arbi_info,
    swap_info,
    accounts_info,
    networks_info,
    reserve_info,
    api_info
)

from web3 import (
    Web3
)
from solcx import compile_source

import requests
from pathlib import Path



class Initializer:
    def __init__(self, network_name, required_minimum_profit):
        self.network_name = network_name
        self.w3 = None
        self.data_collector = None
        self.arbi_transact_creator = None
        self.converter = None
        self.presenter = None
        self.controller = None
        self.required_minimum_profit = required_minimum_profit

        self._initialize_web3(network_name)

    def _initialize_web3(self, network_name):
        network_url = networks_info.networks_infos[network_name]['url']
        self.w3 = Web3(Web3.HTTPProvider(network_url))

    def initialize_data_collector(self):
        swap_contract_instances = {}
        for i in range(0,len(swap_info.swap_addresses)):
            current_dir = Path(__file__).parent
            file_path = current_dir / 'contracts' / swap_info.swap_file_names[swap_info.swap_addresses[i]]
            with open(file_path, 'r') as file:
                contract_source_code = file.read()
            compiled_sol = compile_source(
                contract_source_code,
                output_values=["abi", "bin"],
                solc_version="0.8.26"
            )
            _, contract_interface = compiled_sol.popitem()
            contract_instance = self.w3.eth.contract(
                address=swap_info.swap_addresses[i],
                abi=contract_interface['abi']
            )
            swap_contract_instances[swap_info.swap_addresses[i]] = contract_instance
        
        self.data_collector = DataCollector(
            self.w3,
            swap_contract_instances,
            arbi_info.arbi_intrinsic_gas,
            swap_info.swap_addresses,
            swap_info.swap_function_param_names,
            api_info.etherscan_api_key
        )

    def initialize_arbi_transact_creator(self):
        arbi_contract_instance = self.w3.eth.contract(
            address=arbi_info.arbi_address,
            abi=arbi_info.arbi_abi
        )
        self.arbi_transact_creator = ArbiTransactCreator(
            self.w3,
            accounts_info.accounts_infos[self.network_name][0]['address'],
            accounts_info.accounts_infos[self.network_name][0]['private_key'],
            arbi_contract_instance
        )
    
    def initialize_converter(self):
        ether_usd_rate = self.get_ether_usd_rate_by_api()
        self.converter = Converter(
            ether_usd_rate,
            reserve_info.reserve_infos
        )

    def initialize_presenter(self):
        self.presenter = Presenter()

    def initialize_controller(self):
        self.controller = Controller(
            self.data_collector,
            self.arbi_transact_creator,
            self.converter,
            self.presenter
        )

    def get_ether_usd_rate_by_api(self)->float:
        url = "https://api.coingecko.com/api/v3/simple/price"
        params = {
            "ids": "ethereum",  
            "vs_currencies": "usd"  
        }
    
        response = requests.get(url, params=params)
        response.raise_for_status()
        data = response.json()
        eth_price = data["ethereum"]["usd"]
        return eth_price

        
        


