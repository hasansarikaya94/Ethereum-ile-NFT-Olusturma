from brownie import IIFNFT
from scripts.helpful_scripts import fund_with_link,fund_advanced_coolectible


def main():
    advanced_collectible = IIFNFT[len(IIFNFT) - 1]
    fund_with_link(advanced_collectible.address)