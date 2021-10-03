from os import name
import requests
import sys
import json
from pathlib import Path


def crawl_index(index):
    for resource in index["results"]:
        req_data = {
            "url": resource['url'],
        }

        try:
            req = requests.get(**req_data)
            req.raise_for_status()
            if req.status_code == 200:
                yield req.json()
        except Exception as e:
            print(e)
            print("Cound not get resource", resource["name"], "at url:", resource["url"])


def save_resource(resource, collection_name):
    file_name = f"resource_{resource['id']}.json"
    with Path(f"collections/{collection_name}/{file_name}").open("w") as f:
        json.dump(resource, f, indent=4)


def get_indexes(start=0, end=0):
    for index in Path("indexes").glob("*.json"):
        with index.open("r") as f:
            yield (json.load(f), index.name[:-5])


def main():
    for index, collection_name in get_indexes():
        print("processing collection", collection_name)
        for resource in crawl_index(index):
            #print("element id", resource["id"])
            save_resource(resource, collection_name)


if __name__ == "__main__":
    sys.exit(main())