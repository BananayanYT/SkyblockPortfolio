
class investorData:
    def __init__ (self, name:str, investmentList:list) -> None:
        self.name = name
        self.investmentList = investmentList

    def getName(self) -> str:
        return self.name 

    def getInvestmentList(self) -> list:
        return self.investmentList
    
    # return number of shares for this specific investor object
    def getInvestorShares(self) -> int:
        shares = 0
        investmentList = self.getInvestmentList()
        for investment in investmentList:
            shares += investment[0]
        return shares

"""
TODO:
change iteration through investors to be

listOfInvestorObjects = [[], []]

for investor in listOfInvestorObjects:
     investmentList = investor.getInvestmentList()
     
     #to get shares:
     for sublist in investmentList:
         totalShares += sublist[0]



"""

# format: name, [[shares, NAV Per Share]]
banyaninvest = investorData("Banyan", [[681, 1041666.67], [374, 804054.05], [45, 954920.63], [75, 1201788.71], [63, 1260442.15], [201, 1295251.371], [70, 1253033.052]])
lexinvest = investorData("Lex", [[300, 1041666.67], [24, 1295251.371]])
jonahinvest = investorData("Jonah", [[75, 1041666.67]])
joeyinvest = investorData("J0eyN0obs", [[50, 804054.05], [50, 803921.57], [139, 1201788.71]])


# getters for investment list
def getbanyaninvest():
        return banyaninvest.getInvestmentList()
def getlexinvest():
        return lexinvest.getInvestmentList()
def getjonahinvest():
        return jonahinvest.getInvestmentList()
def getjoeyinvest():
        return joeyinvest.getInvestmentList()


# Dict of names of all investors
investorDict = {
    "Banyan": banyaninvest,
    "Lex": lexinvest,
    "Jonah": jonahinvest,
    "J0eyN0obs": joeyinvest
}


# returns sum of all shares in the hedge fund.  REDUNDANT LUL
def getShares() -> int:
    totalShares = 0
    investmentList = getbanyaninvest() + getlexinvest() + getjonahinvest() + getjoeyinvest() # confirmed this is the correct data
    for sublist in investmentList:
         totalShares += sublist[0]

    #print(totalShares)
    return totalShares




    # DICT ACCESSING:
    #.keys() for keys
    #.items() for both
    #.values() for only values


    # Investor Gets
    #print(banyaninvest.getName())
    #print(banyaninvest.getInvestmentList()[x][y]) where x is the index of the list within the list of lists, and y is the index in the lower list.

#workingPortfolioCode.main()