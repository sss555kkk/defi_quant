

from web3 import Web3

from CDI.setting import (
    accounts_info,
    networks_info
)
from CDI.contract_deploy_interactor import (
    ContractDepoloyInteractor,
)


def create_cdi(network_name):
    network_url = networks_info.networks_infos[network_name]['url']
    w3 = Web3(Web3.HTTPProvider(network_url))
    cdi = ContractDepoloyInteractor(
        w3,
        networks_info.networks_infos[network_name],
        accounts_info.accounts_infos[network_name]
    )
    return cdi


    

