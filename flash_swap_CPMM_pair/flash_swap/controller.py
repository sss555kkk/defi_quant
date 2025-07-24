

from flash_swap.arbi_finder import (
    find_pair
)
from flash_swap.priority_optimizer import (
    optimize_priority
)
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


class Controller:
    def __init__(
        self,
        data_collector:DataCollector,
        transact_creator:ArbiTransactCreator,
        converter:Converter,
        presenter:Presenter,
        required_minimum_profit:int
    )->None:
        self.data_collector = data_collector
        self.transact_creator = transact_creator
        self.converter = converter
        self.presenter = presenter
        self.required_minimum_profit = required_minimum_profit

    def start_search(self)->None:
        is_swap_pair_profitable, swap_pair_info = self.determine_arbi_possible_using_swap_pair_info()
        if not is_swap_pair_profitable:
            return 
        is_transact_profitable, transact_info = self.determine_arbi_possible_using_fee_info(swap_pair_info)
        if not is_transact_profitable:
            return
        self.start_arbi_transact(transact_info)

    def determine_arbi_possible_using_swap_pair_info(self):
        swap_reserve_data = self.get_all_swap_pairs_data()
        swap_pair_info = find_pair.get_max_profit_arbitrage_opportunity(
            swap_reserve_data
        )
        if swap_pair_info['max_profit'] > 0:
            return True, swap_pair_info
        else:
            return False, None

    def determine_arbi_possible_using_fee_info(self, swap_pair_info):        
        intrinsic_gas = self.data_collector.get_intrinsic_gas()
        base_fee, priority_fee = self.data_collector.get_base_fee_and_priority_fee()

        is_profit_larger = self.is_profit_larger_than_required_minimum_profit(
            swap_pair_info['max_profit'], 
            intrinsic_gas,
            base_fee,
            priority_fee
        )
        if is_profit_larger:
            transact_info = swap_pair_info.copy()
            transact_info['intrinsic_gas'] = intrinsic_gas
            transact_info['base_fee'] = base_fee
            transact_info['priority_fee'] = priority_fee
            transact_info['wei_to_usd_rate'] = self.converter.get_wei_to_usd_rate()
            return True, transact_info
        else: 
            return False, None
        
    
    def get_all_swap_pairs_data(self)->list:
        reserve_data = self.data_collector.get_all_swap_pairs_data()
        for data in reserve_data:
            for i in range(0,2):
                data[i] = self.converter.convert_fixed_point_to_float(
                    i,
                    data[i]
                )
        return reserve_data
    
    def is_profit_larger_than_required_minimum_profit(
        self, 
        profit:float, 
        gas:int,
        fee_1:int, 
        fee_2:int
    )->bool:
        costs_as_usd = self.converter.convert_gwei_to_usd(gas*(fee_1+fee_2))
        is_profitable = (profit - costs_as_usd) > self.required_minimum_profit
        return is_profitable
    
    def start_arbi_transact(
        self,
        transact_info:dict
    )->None:
        optimized_transact_info = self.optimize_priority_fee(
            transact_info
        )
        result_from_transact = self.transact_creator.start_transact_creating(
            optimized_transact_info
        )
        self.presenter.send_transact_result(
            optimized_transact_info,
            result_from_transact
        )

    def optimize_priority_fee(
        self, 
        swap_pair_info:dict
    )->dict:
        optimized_transact_info = optimize_priority.optimize_priority_fee(
            swap_pair_info
        )
        return optimized_transact_info




        

