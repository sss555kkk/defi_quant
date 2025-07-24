

from flash_swap.arbi_finder.swap_reserves import (
    SwapReserves
)

from math import (
    ceil,
    floor
)
from typing import (
    Tuple
)


def search_max_profit_t0_and_swap_order(
    swap_0:SwapReserves, 
    swap_1:SwapReserves
)->dict:
    swap_first, swap_second = classfy_swaps_order(swap_0, swap_1)
    if swap_first.ratio == swap_second.ratio:
        swap_pair_info = {
            'swap_first_address': None,
            'swap_second_address': None,
            't0_optimal': None,
            'max_profit': 0
        }
        return swap_pair_info
    
    t0_balanced = find_t0_to_make_swap_ratio_equal_target_ratio(
        swap_first, 
        swap_second.ratio
    )
    t0_optimal, max_profit = search_max_profit_t0(
        swap_first, 
        swap_second,
        t0_balanced
    )
    swap_pair_info = {
        'swap_first_address': swap_first.address,
        'swap_second_address': swap_second.address,
        't0_optimal': t0_optimal,
        'max_profit': max_profit
    }
    return swap_pair_info

def classfy_swaps_order(
    swap_0:SwapReserves, 
    swap_1:SwapReserves
)->Tuple[SwapReserves,SwapReserves]:
    swap_first, swap_second = (
        (swap_0, swap_1) 
        if (swap_0.ratio <= swap_1.ratio) 
        else (swap_1, swap_0)
    )
    return swap_first, swap_second

def find_t0_to_make_swap_ratio_equal_target_ratio(
        swap_first:SwapReserves, 
        target_ratio:float
    )->int:
    required_t0 = swap_first.get_required_amount_of_t0_for_target_ratio(
        target_ratio
    )
    return ceil(required_t0)

def search_max_profit_t0(
    swap_first:SwapReserves,
    swap_second:SwapReserves,
    t0_initial:int
)->Tuple[int,float]:
    t0_start = t0_initial
    t0_end = 0
    t0_step = 0
    max_profit=0
    while is_t0_range_larger_than_2(t0_start, t0_end):
        t0_step = make_step(t0_start, t0_end)
        new_t0_start, new_t0_end, new_max_profit = search_t0_range(
            swap_first,
            swap_second,
            t0_start,
            t0_end,
            t0_step
        )
        t0_start = new_t0_start
        t0_end = new_t0_end
        max_profit = new_max_profit
    optimal_t0 = (t0_start + t0_end)/2
    return optimal_t0, max_profit
    
def search_t0_range(
    swap_first:SwapReserves, 
    swap_second:SwapReserves,
    t0_start:float, 
    t0_end:float,
    t0_step:int
)->Tuple[int,int,float]:
    max_profit= float('-inf')
    new_t0_start=0
    new_t0_end=0

    for i in range(t0_start, t0_end, -t0_step):
        profit = calculate_profit_after_two_swap_trade(
            swap_first, 
            swap_second,
            i
        )
        if is_current_profit_larger_than_last_profit(
            profit, 
            max_profit
        ):
            max_profit, new_t0_start = replace_values_with_current_values(
                profit, 
                i
            )
        else:
            new_t0_start += t0_step
            new_t0_end = i
            break
        
    return ceil(new_t0_start), floor(new_t0_end), max_profit  

def calculate_profit_after_two_swap_trade(
    swap_first:SwapReserves, 
    swap_second:SwapReserves,
    t0_input:float
)->float:
    t1_after_first_trade = swap_first.get_expected_swap_output(
        0,
        t0_input
    )
    t0_after_second_trade = swap_second.get_expected_swap_output(
        1,
        t1_after_first_trade
    )
    profit = t0_after_second_trade - t0_input
    return round(profit, 4)

def is_t0_range_larger_than_2(
    t0_start:int, 
    t0_end:int
)->bool:
    is_t0_range_larger = (t0_start-t0_end) > 2
    return is_t0_range_larger

def make_step(
    t0_start:int,
    t0_end:int
)->int:
    range_t0_start_to_end = t0_start-t0_end
    if range_t0_start_to_end < 100:
        return 1
    else:
        step = ceil(range_t0_start_to_end/100)
        return step

def is_current_profit_larger_than_last_profit(
    current_profit:float, 
    last_profit:float
)->bool:
    is_current_profit_larger = current_profit >= last_profit
    return is_current_profit_larger

def replace_values_with_current_values(
    value1:float, 
    value2:float
)->Tuple[float,float]:
    return value1, value2





