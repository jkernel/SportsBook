from bs4 import BeautifulSoup as soup
from urllib.request import urlopen as uReq
import pprint
import json

def footballMain():
    """The first called function.
    Currently calls the only option available, the selectLeague() option.
    Needs building up to offer the selection of multiple options.
    """
    selectedLeague = selectLeague()

    displaySelection(selectedLeague)
    
def selectLeague():
    """Takes  in the availableLeagues dictionary.
    Prompts the user to select a league.
    Returns the key value of theselected league.

    Currently has an extra function for program testing.
    This is the acceptance of options 97-100.
    This function needs to be built into a menu.
    """
    
    print("\n Select a league number to study: \n ")

    for key in availableLeagues:
        print(key)

    leagueSelector = int(input())
    selectedLeague = ""
    for key in availableLeagues:
        if leagueSelector == availableLeagues[key][0]:
            selection = key

    if selection == "":
        print("Invalid selection")
        selectLeague()
        
    # Extra function as described in docstring
    elif selection == "99 Export JSON":
        exportJSONFile()
        footballMain()
    elif selection == "98 Import JSON":
        importJSONFile()
        footballMain()
    elif selection == "97 Display Currently Loaded Data":
        pprint.pprint(leagueData)
        input("Press enter to continue")
        footballMain()
    elif selection == "100 Quit":
        exit()
    # End of extra function
    
    else:
        return selection
    footballMain()

def importJSONFile():
    """ Loads the leagueData.json file into the leagueData dictionary.
    Needs to return the file rather than all be actioned in the function.
    This can only be done properly once the menu system is in place because
    the importJSONFile function is currently being called from within another
    function. This would mean passing the leagueData dictionary down through
    multiple functions rather than directly to this function.
    """
    global leagueData
    print("---LOADING...---")
    with open("leagueData.json") as infile:
        leagueData = json.load(infile)
    print("---LOADED---")
    input("Press enter to continue")
    footballMain()
        
def exportJSONFile():
    """ Saves the leagueData dictionary to a json file called
    leagueData.json.
    Needs to return the file rather than all be actioned in the function.
    This can only be done properly once the menu system is in place because
    the exportJSONFile function is currently being called from within another
    function. This would mean passing the leagueData dictionary down through
    multiple functions rather than directly to this function.
    """
    print("---SAVING...---")
    with open("leagueData.json", "w") as outfile:
        json.dump(leagueData, outfile, indent = 1)
    print("---SAVED---")
    input("Press enter to continue")

def displaySelection(selection):
    """ Takes in the key value of the selected league.
    Prints the league name and number of teams in that league.
    Gives the option of confirming the selection of that league or returning
    to the main menu.
    """
    print("You selected " + selection + "\n")
    print("This will use the following url: " + availableLeagues[selection][1] + "\n")
    print("The league has " + str(availableLeagues[selection][2]) + " teams.")
    choice = int(input("Press 1 to generate this league table or 2 to go back to the main menu."))
    if choice == 1:
        gatherLeagueInfo(selection)
    else:
        footballMain()

def gatherLeagueInfo(selection):
    """ Takes the key of the selected league from the availableLeagues dictionary.
    Scrapes the selected league information from bedstudy.com.
    Calculates unscraped data (for example, total games won).
    Adds all data to the leagueData dictionary.
    Currently assumes the global leagueData dictionary.
    Future upgrades to this function may include:
        * Separate the calculation of additional data to an additional function.
        * Add more calculations (for example, average goals per game) to this
        function or the additional function.
        * Accept an option for previous seasons (other functionality of
        the program would need to be built around that).
    """
    betStudyMain = "https://www.betstudy.com/soccer-stats/"
    season = "c/" #c is current
    fullURL = betStudyMain + season + availableLeagues[selection][1]
    webClient = uReq(fullURL)
    webHTML = webClient.read()
    webClient.close()
    webSoup = soup(webHTML, "html.parser")
    table = webSoup.find("div",{"id":"tab03_"})

    for i in range(1, availableLeagues[selection][2] + 1):
        position = int(table.select('td')[((i-1)*16)].text)
        teamName = table.select('td')[((i-1)*16)+1].text
        homePlayed = int(table.select('td')[((i-1)*16)+2].text)
        homeWon = int(table.select('td')[((i-1)*16)+3].text)
        homeDrew = int(table.select('td')[((i-1)*16)+4].text)
        homeLost = int(table.select('td')[((i-1)*16)+5].text)
        homeFor = int(table.select('td')[((i-1)*16)+6].text)
        homeAgainst = int(table.select('td')[((i-1)*16)+7].text)
        homePoints = int(table.select('td')[((i-1)*16)+8].text)
        awayPlayed = int(table.select('td')[((i-1)*16)+9].text)
        awayWon = int(table.select('td')[((i-1)*16)+10].text)
        awayDrew = int(table.select('td')[((i-1)*16)+11].text)
        awayLost = int(table.select('td')[((i-1)*16)+12].text)
        awayFor = int(table.select('td')[((i-1)*16)+13].text)
        awayAgainst = int(table.select('td')[((i-1)*16)+14].text)
        awayPoints = int(table.select('td')[((i-1)*16)+15].text)
        totalPlayed = homePlayed + awayPlayed
        totalWon = homeWon + awayWon
        totalDrew = homeDrew + awayDrew
        totalLost = homeLost + awayLost
        totalFor = homeFor + awayFor
        totalAgainst = homeAgainst + awayAgainst
        totalPoints = homePoints + awayPoints

        # Add league to the leagueData dictionary if the league does not already exist within it.
        if selection not in leagueData:
            leagueData[selection] = {teamName:
            {"Home":
            {"Played":homePlayed, "Won":homeWon, "Drew":homeDrew, "Lost":homeLost, "For":homeFor, "Against":homeAgainst, "Points":homePoints}
            , "Away":
            {"Played":awayPlayed, "Won":awayWon, "Drew":awayDrew, "Lost":awayLost, "For":awayFor, "Against":awayAgainst, "Points":awayPoints}
            , "Total":
            {"Played":totalPlayed, "Won":totalWon, "Drew":totalDrew, "Lost":totalLost, "For":totalFor, "Against":totalAgainst, "Points":totalPoints}
            }
            }

        # If the league does already exist, just update the teams and statistics.
        else:
            leagueData[selection][teamName] = {"Home":
            {"Played":homePlayed, "Won":homeWon, "Drew":homeDrew, "Lost":homeLost, "For":homeFor, "Against":homeAgainst, "Points":homePoints}
            , "Away":
            {"Played":awayPlayed, "Won":awayWon, "Drew":awayDrew, "Lost":awayLost, "For":awayFor, "Against":awayAgainst, "Points":awayPoints}
            , "Total":
            {"Played":totalPlayed, "Won":totalWon, "Drew":totalDrew, "Lost":totalLost, "For":totalFor, "Against":totalAgainst, "Points":totalPoints}
            }

    input("Press enter to continue.")
    footballMain()

# The availableLeagues dictionary: "League name":["Option number", "League link from betstudy.com", "Number of teams in league"]   
availableLeagues = {"1 English Premier League":[1, "england/premier-league/", 20],
                    "2 English Championship":[2, "england/championship/", 24],
                    "3 English League One":[3, "england/league-one/", 24],
                    "4 English League Two":[4, "england/league-two/", 24],
                    "5 Spanish Primera":[5, "spain/primera-division/", 20],
                    "6 Spanish Segunda":[6, "spain/segunda-division/", 22],
                    "7 Spanish Segunda B":[7, "spain/segunda-b/", 20],
                    "8 French Lique 1":[8, "france/ligue-1/", 20],
                    "9 French Ligue 2":[9, "france/ligue-2/", 20],
                    "10 German Bundesliga":[10, "germany/bundesliga/", 18],
                    "11 German 2 Bundesliga":[11, "germany/2.-bundesliga/", 18],
                    "12 German Liga":[12, "germany/3.-liga/", 20],
                    "13 Italian Serie A":[13, "italy/serie-a/", 20],
                    "14 Italian Serie B":[14, "italy/serie-b/", 19],
                    "15 Brazillian Serie A":[15, "brazil/serie-a/", 20],
                    "16 Brazillian Serie B":[16, "brazil/serie-b/", 20],
                    "17 Argentinian Primera Division":[17, "argentina/primera-division/", 26],
                    "18 Argentinian Prim B Nacional":[18, "argentina/prim-b-nacional/", 25],
                    "19 Argentinian Prim B Metro":[19, "argentina/prim-b-metro/", 20],
                    "97 Display Currently Loaded Data":[97, "", 0],
                    "98 Import JSON":[98, "", 0],
                    "99 Export JSON":[99, "", 0],
                    "100 Quit":[100, "", 0]
                    }
# Initialise the leagueData dictionary
leagueData = {}
