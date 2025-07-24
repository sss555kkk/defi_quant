
import requests

from flash_swap.setting_info import (
    reserve_info,
    api_info
)

class Converter:
    def __init__(
        self, 
        ether_to_usd_rate:float,
        reserve_infos:dict
    ):
        self.ether_to_usd_rate = ether_to_usd_rate 
        self.reserve_infos = reserve_infos

    def convert_fixed_point_to_float(
        self, 
        reserve_index:int, 
        fixed_point_amount:int
    )->float:
        float_amount = (
            fixed_point_amount
            /self.reserve_infos[reserve_index]['decimals']
        )
        return float_amount

    def convert_float_to_fixed_point(
        self, 
        reserve_index:int, 
        float_amount:float
    )->int:
        fixed_point_amount = (
            float_amount
            *self.reserve_infos[reserve_index]['decimals']
        )
        return round(fixed_point_amount)

    def convert_usd_to_wei(self, usd_amount:float)->int:
        wei_amount = usd_amount*10**18/self.ether_to_usd_rate
        return round(wei_amount)

    def convert_wei_to_usd(self, wei_amount:int)->float:
        usd_amount = wei_amount*self.ether_to_usd_rate/10**18
        return usd_amount
    
    
    def get_wei_to_usd_rate(self):
        return self.ether_to_usd_rate/10**18








