#!/usr/bin/python3
import os
import requests
import json
from brownie import IIFNFT, network
from metadata import sample_metadata
from scripts.helpful_scripts import get_logo
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()



logo_to_image_uri = {
    "ISTANBUL_1": "https://ipfs.io/ipfs/QmTGQRETtruErCBP5B5rjnVPc88BkiTTHiCn4P6BZz9YZE?filename=istanbul-1.png",
}


def main():
    print("Working on " + network.show_active())
    akilli_kontrat = IIFNFT[len(IIFNFT) - 1]
    number_of_advanced_collectibles = akilli_kontrat.tokenCounter()
    print(
        "The number of tokens you've deployed is: "
        + str(number_of_advanced_collectibles)
    )
    write_metadata(number_of_advanced_collectibles, akilli_kontrat)


def write_metadata(token_ids, nft_contract):
    for token_id in range(token_ids):
        collectible_metadata = sample_metadata.metadata_template
        logo = get_logo(nft_contract.tokenIdToLogo(token_id))
        metadata_file_name = (
            "./metadata/{}/".format(network.show_active())
            + str(token_id)
            + "-"
            + logo
            + ".json"
        )
        if Path(metadata_file_name).exists():
            print(
                "{} already found, delete it to overwrite!".format(
                    metadata_file_name)
            )
        else:
            print("Creating Metadata file: " + metadata_file_name)
            collectible_metadata["name"] = get_logo(
                nft_contract.tokenIdToLogo(token_id)
            )
            collectible_metadata["description"] = "An adorable {} pup!".format(
                collectible_metadata["name"]
            )
            image_to_upload = None
            if os.getenv("UPLOAD_IPFS") == "true":
                image_path = "./img/{}.png".format(
                    logo.lower().replace('_', '-'))
                image_to_upload = upload_to_ipfs(image_path)
            image_to_upload = (
                logo_to_image_uri[logo] if not image_to_upload else image_to_upload
            )
            collectible_metadata["image"] = image_to_upload
            with open(metadata_file_name, "w") as file:
                json.dump(collectible_metadata, file)
            if os.getenv("UPLOAD_IPFS") == "true":
                upload_to_ipfs(metadata_file_name)

# curl -X POST -F file=@metadata/rinkeby/0-SHIBA_INU.json http://localhost:5001/api/v0/add


def upload_to_ipfs(filepath):
    with Path(filepath).open("rb") as fp:
        image_binary = fp.read()
        ipfs_url = (
            os.getenv("IPFS_URL")
            if os.getenv("IPFS_URL")
            else "http://localhost:5001"
        )
        response = requests.post(ipfs_url + "/api/v0/add",
                                 files={"file": image_binary})
        ipfs_hash = response.json()["Hash"]
        filename = filepath.split("/")[-1:][0]
        image_uri = "https://ipfs.io/ipfs/{}?filename={}".format(ipfs_hash, filename)
        print(image_uri)
    return image_uri
