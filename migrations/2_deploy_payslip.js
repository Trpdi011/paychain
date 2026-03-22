const PayslipContract = artifacts.require("PayslipContract");

module.exports = function(deployer) {
  deployer.deploy(PayslipContract);
};