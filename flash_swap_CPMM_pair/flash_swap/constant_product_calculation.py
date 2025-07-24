
from typing import (
    Tuple
)


# SwapReserves 초기값 세팅을 원하는 데로 하기 위한 함수
def calcalate_setting_values(
    initial_reserve_0:float, 
    initial_reserve_1:float, 
    reserve_0_insufficient_quantity:float
)->Tuple[float,float]:
    modified_reserve_0 = initial_reserve_0-reserve_0_insufficient_quantity
    modified_reserve_1 = initial_reserve_0*initial_reserve_1/modified_reserve_0
    return modified_reserve_0, modified_reserve_1




