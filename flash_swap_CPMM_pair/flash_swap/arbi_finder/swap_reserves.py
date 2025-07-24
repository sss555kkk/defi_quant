
from typing import (
    Tuple
)
from math import sqrt

class SwapReserves:
    def __init__(
        self, 
        address:str, 
        t0:float=0, 
        t1:float=0
    ):
        self.address = address
        self.t0 = t0
        self.t1 = t1
        self.k = 0
        self.ratio = 0

        self.set_k_and_ratio()
        
    def get_expected_swap_output(
        self, 
        token_number:int, 
        amount:float
    )->float:
        reserve_in, reserve_out = self.classify_reserve_in_and_out(token_number)
        amount_token_out = self.calculate_swap_output(amount, reserve_in, reserve_out)
        return amount_token_out
    
    def classify_reserve_in_and_out(
        self,
        token_number:int
    )->Tuple[float,float]:
        (reserve_in, reserve_out) = (
            (self.t0, self.t1) 
            if token_number==0 
            else (self.t1, self.t0)
        )
        return reserve_in, reserve_out
            
    def calculate_swap_output(
        self, 
        amount_in:float,
        reserve_in:float,
        reserve_out:float
    )->float:
        amount_out = amount_in*reserve_out/(amount_in+reserve_in)
        return amount_out
    
    def get_required_amount_of_t0_for_target_ratio(
        self, 
        target_ratio:float
    )->float:
        if self.ratio == target_ratio:
            return 0
        balanced_t0 = sqrt(self.k*target_ratio)
        required_amount_of_t0 = balanced_t0 - self.t0
        return required_amount_of_t0
    
    def set_reserves(self, t0:float, t1:float)->None:
        self.t0 =  t0
        self.t1 =  t1
        self.set_k_and_ratio()

    def set_k_and_ratio(self)->None:
        self.k = self.t0*self.t1
        self.ratio = 0 if self.t0 == 0 else self.t0/self.t1

    def get_reserves(self)->Tuple[float,float]:
        return (self.t0, self.t1)



