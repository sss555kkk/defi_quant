
from flash_swap.arbi_finder import (
    find_pair
)


def test_find_t0():
    ...

def test_find_pair():
    reserve_data = [
        ['a',10000,10000],
        ['b',9900, 10101.0101010101],
        ['c',9800, 10204.081632653062],
        ['d',9100, 10989.010989010989],
        ['e',9000, 11111.111111111111]
    ]

    result = find_pair.get_max_profit_arbitrage_opportunity(reserve_data)
    return result



result = test_find_pair()
print (result)

