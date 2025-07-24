

from flash_swap.arbi_finder import (
    find_t0
)
from flash_swap.arbi_finder.swap_reserves import (
    SwapReserves,
)

from itertools import (
    combinations
)


def get_max_profit_arbitrage_opportunity(
    swap_list:list
)->dict:
    swap_reserves = convert_list_to_swap_reserves(swap_list)
    max_profit_pair = {
        'swap_first_address': None,
        'swap_second_address': None,
        't0_optimal': None,
        'max_profit': 0
    }
    swap_pairs = combinations(swap_reserves, 2)
    for swap_pair in swap_pairs:
        new_swap_pair_info = (
            find_t0.search_max_profit_t0_and_swap_order(*swap_pair)
        )
        if is_current_profit_larger_than_last_profit(
            new_swap_pair_info['max_profit'], 
            max_profit_pair['max_profit']
        ):
            max_profit_pair = replace_max_pair_with_new_pair(new_swap_pair_info)
        
    return max_profit_pair

def convert_list_to_swap_reserves(
    swap_list:list
)->list:
    swap_reserves = []
    for swap_data in swap_list:
        new_swap_reserve = SwapReserves(*swap_data)
        swap_reserves.append(new_swap_reserve)
    return swap_reserves

def is_current_profit_larger_than_last_profit(
    current_profit:float, 
    last_profit:float
)->bool:
    is_current_profit_larger = current_profit >= last_profit
    return is_current_profit_larger

def replace_max_pair_with_new_pair(new_pair:dict)->dict:
    return new_pair








