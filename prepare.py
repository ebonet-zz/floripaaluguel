import codecs

import requests, json
import unicodecsv as csv

def perform_paged_request(page):
    """
    Query a single page of the Viva Real API.

    :param page the page index to be queried

    :return a dictionary representation of the data queried
    """
    url = "http://api.vivareal.com/api/1.0/locations/listings"
    params = {
        "apiKey": "183d98b9-fc81-4ef1-b841-7432c610b36e",
        "exactLocation": False,
        "currency": "BRL",
        "business": "RENTA",
        "listingType": "APART",
        "listingUse": "RESIDENCIAL",
        "rankingId":0,
        "locationIds": "BR>Santa Catarina>NULL>Florianopolis",
        "maxResults": 40,
        "page": page
    }


    response = requests.get(url, params=params)
    return json.loads(response.content.decode("utf-8"))

def load_data(max = 100):
    """
    Loads Viva Real API listings
    :param out the name of the file to save the results
    :param max max number of pages to load
    """

    current_page = 1

    data = perform_paged_request(current_page)
    listings = []

    while current_page < max and data and data["listings"]:
        print(current_page)
        listings = listings+data["listings"]
        current_page += 1
        data = perform_paged_request(current_page)

    return listings

def extractInfo(listings):
    """
    Extracts interesting rental data from the listing objects

    :param listings the path for the input file
    :return they properties in the new dictionary and a list of the transformed object
    """

    keys = ["propertyId", "rentPrice", "area", "bathrooms", "rooms",
            "garages", "latitude", "longitude", "address", "suites",
            "rentPeriodId", "condominiumPrice", "iptu"]

    return keys, [{k: rental[k] for k in keys} for rental in listings]
#
# with open("rentals.csv", "w") as csvFile:
#     data = load_data()
#     keys, data = extractInfo(data)
#     writer = csv.DictWriter(csvFile, encoding="utf-8", fieldnames=keys, quoting=csv.QUOTE_ALL)
#     writer.writeheader()
#     writer.writerows(data)


with open("rentals_small.json", "w") as jsonFile:
    data = load_data(max=10)
    json.dump(data, jsonFile)