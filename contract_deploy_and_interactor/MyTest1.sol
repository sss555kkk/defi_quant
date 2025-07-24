// SPDX-License-Identifier: MIT
pragma solidity ^0.8.26;

contract MyTest1 {
    uint256 number1 = 100;

    function getNumber1() external view returns(uint256)
    {
        return number1;
    }
    
    function setNumber1(uint256 _number) external returns(uint256)
    {
        number1 = _number;
        return number1;
    }
}