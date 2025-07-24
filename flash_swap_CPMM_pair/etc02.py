
"""
build transaction의 모든 매개변수



unsent_tx = my_contract_instance.functions.mint(ACCOUNT_1_ADDRESS, 1000).build_transaction({
    "from": ACCOUNT_1_ADDRESS,
    "nonce": w3.eth.get_transaction_count(ACCOUNT_1_ADDRESS),
    "maxFeePerGas": Web3.to_wei(100, "gwei"),  # 최대 가스 요금
    "maxPriorityFeePerGas": Web3.to_wei(2, "gwei"),  # 검증자에게 지불할 팁
    "gas": 300000,  # 가스 한도
    "chainId": 1,  # Ethereum Mainnet
})
"""


# 