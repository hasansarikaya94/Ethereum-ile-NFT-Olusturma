from brownie import IIFNFT, accounts, network, config


def main():
    dev = accounts.add(config['wallets']['from_mnemonic'])
    print(dev)