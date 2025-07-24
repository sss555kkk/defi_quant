

// SPDX-License-Identifier: MIT
pragma solidity ^0.8.26;

import {ISwap} from './ISwap.sol';

contract Swap2 is ISwap {

    uint256 public amountOfReserve0=9000e18;
    uint256 public amountOfReserve1=11111.111111111111e18;


    function getToken0() external view returns(uint256) 
    {
        return amountOfReserve0;
    }

    function getToken1() external view returns(uint256) 
    {
        return amountOfReserve1;
    }

}