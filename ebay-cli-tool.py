import urllib3
import json
import statistics
import itertools


def main():


    ## ENTER APP NAME GIVEN BY EBAY HERE
    APP_NAME = str(input("Please enter your eBay app ID: "))
    ENTRIES_PER_PAGE = '100'

    ROOT_URL = 'http://svcs.ebay.com/services/search/FindingService/v1?OPERATION-NAME=findCompletedItems&SERVICE-NAME=FindingService&SERVICE-VERSION=1.11.0&paginationInput.entriesPerPage=' + ENTRIES_PER_PAGE + '&RESPONSE-DATA-FORMAT=JSON&GLOBAL-ID=EBAY-US&REST-PAYLOAD&SECURITY-APPNAME='+APP_NAME

    keyword = str(input("Please enter a keyword to search: "))

    final_url = ROOT_URL + '&keywords=' + keyword

    print("Final url: ", final_url)

    ## URLLib3
    http = urllib3.PoolManager()
    response = http.request('GET', final_url)

    # Determine Success

    if str(response.status) == '200':
        print("Request successful...")
    else:
        print("Something went wrong")
        print(response.status)

    ## Decode into json
    res_json = json.loads(response.data.decode('utf-8'))
    price_data = res_json["findCompletedItemsResponse"][0]["searchResult"]

    ## Access json data requested
    item_count = price_data[0]['@count']
    print("{} results found: ".format(item_count))

    ## Acces items
    prices, listings = get_items(price_data)
    

    ####Get Stats

    ## Mean Price
    mean = get_mean_price(prices)
    print("Mean: $", mean)

    ## Median Price
    median = get_median_price(prices)
    print("Median Price: $", median)

    ## Max Price
    max_price = get_max_price(prices)
    print("Maximum price: $", max_price)

    ## Min Price
    min_price = get_min_price(prices)
    print("Minimum price: $", min_price)

    ### Create dict of item titles with corresponding prices
    ## Call to create_title_price_dict function and print info

    

## Takes data from response and how many items found
def get_items(data):
    items = len(data[0]["item"])
    listings = []
    prices = []

    for i in range(items):
        name_data = data[0]["item"][i]["title"]
        price_data = data[0]["item"][i]["sellingStatus"][0]["currentPrice"][0]["__value__"]
        prices.append(price_data)
        listings.append(name_data)

    prices = [float(number) for number in prices]
    return prices, listings

## Determine mean of price data
def get_mean_price(price_data):

    mean_price = statistics.mean(price_data)
    # print("Mean price: ", mean_price)
    return mean_price

## Determine median of price data
def get_median_price(prices):
    
    median = statistics.median(prices)
    return median

## Determine maximum value of price data
def get_max_price(prices):
    max_price = max(prices)

    return max_price

def get_min_price(prices):
    min_price = min(prices)

    return min_price

## FIX: splitting by character and not by complete title
# def create_title_price_dict(prices, listings):

    
#     listings = ",".join(itertools.chain(*listings))
#     items_dict = dict(zip(listings, prices))
#     return items_dict


main()






