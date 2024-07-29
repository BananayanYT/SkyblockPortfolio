import investorDataFunctions

#   investorList: list of lists of investments [[shares,NAV Per Share], [shares,NAV Per Share]]
# sharestoRemove: number of shares that the person is removing from the portfolio
# portfolioValue: current NAV of the portfolio
def calculatePayout(investorList, sharestoRemove, portfolioValue) -> float:
    initialinvestment = 0 # total number of shares owned by this investor (1 share per million invested)
    newInvestmentValue = 0 # the amount the investor's money has made.

    initialInvestmentValue = 0 # the coin amount they invested

    TheInvestorisEntitledto = 0



    payout = 0 # amount to pay out to the investor
    myProfit = 0 # the amount of money I make (stays in the fund)




    for investment in investorList:
        initialinvestment += (investment[0])  # Get shares from the investorList

    totalShares = investorDataFunctions.getShares() # total number of shares in circulation

    coininvestment = (initialinvestment * 1000000)

    # calculate live NAV Per Share:
    NAVPerShare = portfolioValue / totalShares

    # calculate the current value of their shares:
    shareValue = NAVPerShare * sharestoRemove

    # calculate the current value of their shares
    newInvestmentValue = initialinvestment * NAVPerShare

    # calculate the change in their money
    capitalGain = newInvestmentValue - (initialinvestment * 1000000)

    betterpayout =  (initialinvestment * 1000000) + (0.25 * (newInvestmentValue - coininvestment) ) #formula

    # need extra variable to track the difference in values
    
    # calculate amount to payout
    # payout = newInvestmentValue + (capitalGain * 0.25)
    TheInvestorisEntitledto = (initialinvestment * 1000000) + (0.25 * (newInvestmentValue - coininvestment) ) # THE MAGFIC NUMBVER I DID IT WOOOOOOooooooooooo!!!!
    print("The Investor is Entitled to: {:,}".format(TheInvestorisEntitledto))

    # calculate my profit
    myProfit = (capitalGain * 0.75)
    print("(remains in fund) Banyan Profit: {:,}".format(myProfit) + "\n\n\n")

    return payout

# NAV: Net Asset Value
# NAV = TOTAL Valuation of Assets

# NAV Per Share: NAV/(TOTAL # of shares issued)

# (portfolio NAV)/(# of shares in circulation)
def getcurrentNAVPerShare(portfolioNAV):
    shareCount = investorDataFunctions.getShares()
    # portfolioNAV = | need to calculate this here eventually, but for now ill just pass it in.

    currNAVPerShare = portfolioNAV / shareCount

    return currNAVPerShare





#investorProfitCalculator.getcurrentNAVPerShare(portfolioNAV)
# ALGO:
"""
algorithm:
For each investment amount:

based on investment amount, calculate number of shares to allocate (1 share per million invested)

then calculate the NAV value on those shares:
NAV per share: NAV/(TOTAL # of shares issued)

store both of these values together in the investor object. (will have to refer to them as a pair later to calculate the extracted value of the money)

then when this person desires to remove their money:

calculate (their shares) * (current NAV per share) = the accrued value on their money

then calulate the amount their money has increased:
ex: 300m in, worth 500m now.  the change is 200m

then calculate my fee, which is 75% of the change
ex: 200*.75 = 150m

the amount they're entitled to is: 
their initial investment + the remaining 25% of the change

and the other 75% stays in the fund.
"""


#workingPortfolioCode.main()