


class ArbiTransactCreator:
    def __init__(
        self,
        web3_instance,
        account_address,
        account_private_key,
        arbi_contract_instance
    ):
        self.w3 = web3_instance
        self.account_address = account_address
        self.account_private_key = account_private_key
        self.arbi_contract_instance = arbi_contract_instance

    def start_transact_creating(
        self,
        optimized_transact_info:dict
    )->dict:
        unsent_tx = self.arbi_contract_instance.functions.startArbitrage(
            optimized_transact_info['swap_first_address'],
            optimized_transact_info['swap_second_address'],
            optimized_transact_info['t0_optimal']
        ).build_transaction({
            "from": self.account_address,
            "nonce": self.w3.eth.get_transaction_count(self.account_address),
        })
        signed_tx = self.w3.eth.account.sign_transaction(
            unsent_tx, 
            private_key=self.account_private_key
        )
        tx_hash = self.w3.eth.send_raw_transaction(signed_tx.rawTransaction)

        # 여기서부터 transact 성공, 실패 시에 따라서 값을 읽어와서 반환해야 함.
        # 실패 시에는 이미 보낸 transact을 취소해야 함.
        tx_receipt = self.w3.eth.wait_for_transaction_receipt(tx_hash)





        

    