pragma solidity ^0.8.0;

contract Contract {
    address public customer;
    address public owner;
    address public courier;
    uint256 public price;
    bool public paid;

    constructor(address ownerAddress, address customerAddress, uint256 priceOfOrder) {
        owner = ownerAddress;
        customer = customerAddress;
        courier = address(0);
        price = priceOfOrder;
        paid = false;
    }

    function payForOrder() external payable {
        paid = true;
    }

    function addCourier(address courierAddress) external {
        courier = courierAddress;
    }

    function confirmDelivery() external {
        uint256 ownerMoney = (price * 80) / 100;
        uint256 courierMoney = (price * 20) / 100;

        payable(owner).transfer(ownerMoney);
        payable(courier).transfer(courierMoney);
    }
}
