// SPDX-License-Identifier: MIT
pragma solidity ^0.8.26;

interface ISwap {

    function getToken0() external view returns(uint256);

    function getToken1() external view returns(uint256);
}