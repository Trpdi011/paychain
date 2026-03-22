// SPDX-License-Identifier: MIT
pragma solidity ^0.8.19;

contract PayslipContract {

    address public hrAdmin;

    struct Payslip {
        uint256 employeeId;
        string  employeeName;
        string  company;
        uint256 basicSalary;
        uint256 netPay;
        uint256 month;
        uint256 year;
        string  payslipHash;
        uint256 timestamp;
    }

    mapping(uint256 => Payslip[]) private payslips;

    event PayslipGenerated(
        uint256 employeeId,
        uint256 netPay,
        string  payslipHash,
        uint256 timestamp
    );

    constructor() {
        hrAdmin = msg.sender;
    }

    modifier onlyHR() {
        require(msg.sender == hrAdmin, "Only HR!");
        _;
    }

    function generatePayslip(
        uint256 _empId,
        string memory _name,
        string memory _company,
        uint256 _basicSalary,
        uint256 _netPay,
        uint256 _month,
        uint256 _year,
        string memory _hash
    ) public onlyHR {
        payslips[_empId].push(Payslip(
            _empId,
            _name,
            _company,
            _basicSalary,
            _netPay,
            _month,
            _year,
            _hash,
            block.timestamp
        ));
        emit PayslipGenerated(_empId, _netPay, _hash, block.timestamp);
    }

    function getPayslip(uint256 _empId, uint256 _index)
        public view returns (Payslip memory) {
        return payslips[_empId][_index];
    }

    function getPayslipCount(uint256 _empId)
        public view returns (uint256) {
        return payslips[_empId].length;
    }

    function verifyPayslip(uint256 _empId, string memory _hash)
        public view returns (bool) {
        for (uint i = 0; i < payslips[_empId].length; i++) {
            if (keccak256(bytes(payslips[_empId][i].payslipHash)) ==
                keccak256(bytes(_hash))) {
                return true;
            }
        }
        return false;
    }
}