from brownie import IIFNFT, accounts, config
from scripts.helpful_scripts import get_logo,fund_with_link
import time



def main():

    dev = accounts.add(config["wallets"]["from_key"])
    akilli_kontrat = IIFNFT[len(IIFNFT) - 1]
    
    transaction = akilli_kontrat.createCollectible("None", {"from": dev})

    print("Waiting on second transaction...")
    transaction.wait(1)
    time.sleep(5)

    requestId = transaction.events['requestedCollectible']['requestId']
    token_id = akilli_kontrat.requestIdToTokenId(requestId)
    logo  = get_logo(akilli_kontrat.tokenIdToLogo(token_id))

    print('Logo of tokenId {} is {}'.format(token_id, logo))


