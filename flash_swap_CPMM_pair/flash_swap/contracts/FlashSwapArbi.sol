// SPDX-License-Identifier: MIT
pragma solidity ^0.8.26;

import {IFlashSwapArbi} from './IFlashSwapArbi.sol';


contract FlashSwapArbi is IFlashSwapArbi {
    
    function stratArbiTransaction(
        uint256 t0Amount, 
        address swapFirst, 
        address swapSecond
    )
        external returns(uint256) 
    {
        return t0Amount;
    }

    function sendTokenToOwner(
        address tokenAddress,
        uint256 amount,
        address _to
    )
        external {}
}