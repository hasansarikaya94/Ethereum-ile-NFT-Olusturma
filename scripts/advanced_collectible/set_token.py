#!/usr/bin/python3
from brownie import SimpleCollectible, IIFNFT, accounts, network, config
from metadata import sample_metadata
from scripts.helpful_scripts import get_logo, OPENSEA_FORMAT


logo_metadata_dic = {
    "ISTANBUL_1": "https://ipfs.io/ipfs/QmcWbjsF4qYRVkUpqXrN7uvUs2rpPmkpAcJxcs4V4gzdNx?filename=0-ISTANBUL_1.json", 
    "ISTANBUL_2": "https://ipfs.io/ipfs/QmcWbjsF4qYRVkUpqXrN7uvUs2rpPmkpAcJxcs4V4gzdNx?filename=0-ISTANBUL_1.json"
}

def main():
    print("Working on " + network.show_active())
    akilli_kontrat = IIFNFT[len(IIFNFT) - 1]
    number_of_advanced_collectibles = akilli_kontrat.tokenCounter()
    print(
        "The number of tokens you've deployed is: "
        + str(number_of_advanced_collectibles)
    )
    for token_id in range(number_of_advanced_collectibles):
        logo = get_logo(akilli_kontrat.tokenIdToLogo(token_id))
        if not akilli_kontrat.tokenURI(token_id).startswith("https://"):
            print("Setting tokenURI of {}".format(token_id))
            set_tokenURI(token_id, akilli_kontrat,logo_metadata_dic[logo])
        else:
            print("Skipping {}, we already set that tokenURI!".format(token_id))


def set_tokenURI(token_id, nft_contract, tokenURI):
    dev = accounts.add(config["wallets"]["from_key"])
  

    nft_contract.setTokenURI(token_id, tokenURI, {"from": dev})

    print(
        "Awesome! You can view your NFT at {}".format(
            OPENSEA_FORMAT.format(nft_contract.address, token_id)
        )
    )
    print('Please give up to 20 minutes, and hit the "refresh metadata" button')
