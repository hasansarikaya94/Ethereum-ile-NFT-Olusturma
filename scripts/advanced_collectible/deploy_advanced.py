from brownie import IIFNFT, accounts, network, config
from scripts.helpful_scripts import fund_with_link, fund_advanced_coolectible

def main():
    dev = accounts.add(config['wallets']['from_key'])
    print(network.show_active())

    publish_source = False 
    akilli_kontrat = IIFNFT.deploy(
        config["networks"][network.show_active()]['vrf_coordinator'],
        config["networks"][network.show_active()]['link_token'],
        config["networks"][network.show_active()]['keyhash'],
        {"from": dev},

        publish_source = publish_source,
    )
    fund_advanced_coolectible(akilli_kontrat)
    return akilli_kontrat