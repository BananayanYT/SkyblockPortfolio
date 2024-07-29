import pandas as pd
import requests
from concurrent.futures import ThreadPoolExecutor
import matplotlib.pyplot as plt
from datetime import date, timedelta

import investorProfitCalculator
import investorDataFunctions


# current portfolio 7/17/24 at 11am
search_dict = {
    'Rose Dye': 3,
    'Sand Castle Barn Skin': 4,
    'Real Grandma Wolf Skin': 2,
    'Portal Dye': 5,
    'Ancient Golden Dragon Skin': 1,
    'Ivory Black Cat Skin': 1,
    'Onyx Black Cat Skin': 1,
    'Black Plushie Elephant Skin': 1,
    'Albino Scatha Skin': 1,
    'Cosmic Elephant Skin': 1,
    'Midnight Dolphin Skin': 4,
}


# Change this to a dictionary with individual acquisition costs
combinedAcquisitionCost = {
    'Rose Dye': 256500000,
    'Sand Castle Barn Skin': 161800000,
    'Black Plushie Elephant Skin': 145000000,
    'Real Grandma Wolf Skin': 220000000,
    'Ivory Black Cat Skin': 170000000,
    'Onyx Black Cat Skin': 237999999,
    'Ancient Golden Dragon Skin': 262000000,
    'Portal Dye': 374200000,
    'Albino Scatha Skin': 137000000,
    'Cosmic Elephant Skin': 245000000,
    'Midnight Dolphin Skin': 264900000,
}


# Function to fetch auction house data for a given page
def fetch_auction_house(page_number: int, url: str) -> pd.DataFrame:
    response = requests.get(f'{url}?page={page_number}')
    auctions_data = response.json()['auctions']
    df = pd.DataFrame(auctions_data)
    return df


# Clean DataFrame and format timestamps
def clean_dataframe(df: pd.DataFrame) -> pd.DataFrame:
    df.drop(columns=['auctioneer', 'profile_id', 'coop', 'extra', 'item_lore', 'item_bytes', 'claimed_bidders', 'item_uuid', 'bids'], inplace=True)
    df['start'] = pd.to_datetime(df['start'], unit='ms')
    df['end'] = pd.to_datetime(df['end'], unit='ms')
    df['last_updated'] = pd.to_datetime(df['last_updated'], unit='ms')
    desired_order = ['item_name', 'tier', 'uuid', 'starting_bid', 'highest_bid_amount', 'category', 'start', 'end', 'last_updated', 'claimed', 'bin']
    df = df[desired_order]
    return df


# Use ThreadPoolExecutor to fetch pages concurrently
def fetch_all_pages_concurrently(total_pages: int, url: str) -> pd.DataFrame:
    with ThreadPoolExecutor(max_workers=15) as executor:
        futures = [executor.submit(fetch_auction_house, i, url) for i in range(total_pages)]
        result = pd.concat([future.result() for future in futures], ignore_index=True)
    return result


def find_item_lbin(df: pd.DataFrame, item_name: str) -> pd.DataFrame:
    # Filter by name
    filtered_df = df[df['item_name'] == item_name]
    # Sort by the values in starting_bid
    filtered_df = filtered_df.sort_values(by=['starting_bid'])
    # Query works like an if which allows us to search for rows where bin == True and claimed == False
    filtered_df = filtered_df.query('bin == True and claimed == False')
    # Because the DF is sorted by starting_bid, we can return the first row and that will be the lbin
    filtered_df = filtered_df.head(1)
    # Set uuid in filtered_df to be command version /viewauction + uuid
    filtered_df.loc[:, 'uuid'] = '/viewauction ' + filtered_df['uuid'].astype(str)
    if filtered_df.empty:
        return pd.DataFrame(columns=df.columns)
    return filtered_df


# This needs to make an API request and calculate the current portfolio valuation based on lbins.
def getPortfolioValue():
    return 0


# Loop through Dictionary
# This is a helper function that works with find_item_lbin
# NOTES: This function returns an appended DataFrame
# Uses search_dict above as the search criteria
def find_item_lbin_helper(df: pd.DataFrame) -> pd.DataFrame:
    df4 = pd.DataFrame(columns=df.columns)
    for item_name in search_dict.keys():
        # Call find_item_lbin and set result equal to it
        result = find_item_lbin(df, item_name)
        # Concat result to current working DataFrame
        df4 = pd.concat([df4, result], ignore_index=True)
    return df4



totalCurrentValue = 0 # NAV of Portfolio Right now
currentPortfolioProfit = 0
url = "https://api.hypixel.net/skyblock/auctions"
df4 = pd.DataFrame()


def APIStuff():
    global totalCurrentValue, currentPortfolioProfit, df4

    url = "https://api.hypixel.net/skyblock/auctions"
    r = requests.get(url).json()
    total_pages = int(r['totalPages'])
    df3 = fetch_all_pages_concurrently(total_pages, url)
    df = clean_dataframe(df3)
    df4 = pd.DataFrame(columns=df.columns)

    lbin_df = find_item_lbin_helper(df)
    find_item_test = dict(zip(lbin_df['item_name'], lbin_df['starting_bid']))

    for lbinKey, lbinValue in find_item_test.items():
        for acqKey, acqValue in combinedAcquisitionCost.items():
            if lbinKey == acqKey:
                currentValue = lbinValue * search_dict[lbinKey]
                currentProfit = currentValue - acqValue
                totalCurrentValue += currentValue
                print("\nName: " + lbinKey)
                print("Owned: " + str(search_dict[lbinKey]))
                print("LBIN: {:,}".format(lbinValue))
                print("Current Profit: {:,}".format(currentProfit))

    import investorDataFunctions
    allCurrentInvestmentInputs = investorDataFunctions.getShares() * 1000000
    currentPortfolioProfit = totalCurrentValue - allCurrentInvestmentInputs



# return the amount the investor's money has increased in value by (curr - past) 
def getInvestorProfit() -> int:
     sumShares = investorDataFunctions.getShares()
     currNAVPerShare = int(investorProfitCalculator.getcurrentNAVPerShare(totalCurrentValue))
     
    # return = (sum(investor shares) * Current NAV Per Share) - (SUM(initial investments of all investors))
     investorProfit = ((sumShares * 1000000) * (currNAVPerShare)) - (sumShares * 1000000)
     return investorProfit





def main():

    APIStuff()

    print("\n\nTotal Portfolio Value: {:,}".format(totalCurrentValue))
    print("Total Fund Profit:  {:,}".format(currentPortfolioProfit))
    print("-------------------------------------------------------")


    # Data:
    currNAVPerShare = investorProfitCalculator.getcurrentNAVPerShare(totalCurrentValue)
    ban_investor = investorDataFunctions.investorDict["Banyan"]
    banyanShares = ban_investor.getInvestorShares()
    totalShares = investorDataFunctions.getShares()
    banyanShareValue = (currNAVPerShare * banyanShares) # value of my shares
    investorGrowth = ((totalShares - banyanShares) * currNAVPerShare)
    totalInitialInvestmenbyOthers = ((totalShares - banyanShares) * 1000000)
    profitFromOtherInvestorGrowth = (0.75 * (investorGrowth - totalInitialInvestmenbyOthers))
    banyanInitInvestment = banyanShares * 1000000




    banyanValue = ((currNAVPerShare * banyanShares) + (0.75 * (investorGrowth - totalInitialInvestmenbyOthers)) )    # BV = value of my shares + (0.75 * (sum(current value of investor shares) - sum(initial investments))

    banyanProfit = (banyanShareValue - banyanInitInvestment)



    print("hmmmm, a lot of focus on yourself...")
    print("- John")
    print("\n")
    print("Banyan's Share Value: {:,}".format(banyanShareValue))
    print("Banyan Profit From Other Investors: {:,}".format(profitFromOtherInvestorGrowth))
    print("-------------------------------------------------------\n\n")


    print("Total Value Owned By Banyan: {:,}".format(int(banyanValue)))
    print("Banyan's Total Profit: {:,}".format(banyanProfit))
    print("-------------------------------------------------------")
    print("\n\n")




    #.keys() for keys
    #.items() for both
    #.values() for only values

    
    print("Testing investment removal")
    # test: calculate payout if lex removes 300 shares

    # Pass the correct investor object from the dictionary

    lex_investor = investorDataFunctions.investorDict["Lex"]

    payout = investorProfitCalculator.calculatePayout(lex_investor.getInvestmentList(), 300, totalCurrentValue)


# workingPortfolioCode.main
main()