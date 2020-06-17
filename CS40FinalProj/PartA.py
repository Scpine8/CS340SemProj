# Main Menu Options

"""
1. Display cumulative cases and deaths per continent
2. List a country's population, cases, and deaths per month
3. Menu option 3: Calculates the cumulative cases, cumulative deaths,
average cases per capita and average deaths per capita for each line of the original data file (up to that point in time),
then saves this new information as additional columns 12-15 in file partA_output_data.txt.
4. Display stat analysis results per continent
5. Visualize data for 3 countries based on user input (default is greece, china, us),
starting on day of tenth death
6. Exit the program

"""
import random
from tabulate import tabulate
from operator import itemgetter

# First, import a csv

months = {
    1: "January",
    2: "February",
    3: "March",
    4: "April",
    5: "May",
    6: "June",
    7: "July",
    8: "August",
    9: "September",
    10: "October",
    11: "November",
    12: "December"
}

# class DataLine: # TODO: finish this class, move dataLine-related methods to it, adjust organizeFileData
#     def __init__(self, date, day, month, year, cases, deaths, country, continent, population):
#         self.date = date
#         self.day = day
#         self.month = month
#         self.year = year
#         self.cases = cases
#         self.deaths = deaths
#         self.country = country
#         self.continent = continent
#         self.population = population


def organize_file_data():
    line1 = True
    # inputStream = open("partA_input_data.txt")

    dataByCountry = {}
    dataByDate = []

    with open("partA_input_data.txt") as inputStream:
        for line in inputStream:
            if not line1:
                lineSplit = line.split(',')  # split the line into an array of values
                date, day, month, year = lineSplit[0], lineSplit[1], lineSplit[2], lineSplit[3]
                cases, deaths, country, population, continent = lineSplit[4], lineSplit[5], lineSplit[6], lineSplit[9], \
                                                                lineSplit[10]
                # For dataByCountry:
                if continent[-1:] == '\n': # if the csv left a line break at the end
                    country_cont = (country, continent[:-1]) # country is parsed to erase automatic line break
                else:
                    country_cont = (country, continent)
                country_cont_data = [date, day, month, year, cases, deaths, population]

                # Add the keys and values to 'dataByCountry'
                if country_cont not in dataByCountry.keys():
                    dataByCountry[country_cont] = [country_cont_data]
                else:
                    dataByCountry[country_cont].append(country_cont_data)
                # For dataByDate
                date_data = [date, day, month, year, cases, deaths, country, continent, population]
                dataByDate += [date_data]
            else:
                line1 = False
    return [dataByCountry, dataByDate]


def getTotalCasesFromCont(dataLineList):
    cases = 0
    for dataline in dataLineList:
        cases += int(dataline[4])
    return cases


def getTotalDeathsFromCont(dataLineList):
    deaths = 0
    for dataline in dataLineList:
        deaths += int(dataline[5])
    return deaths

def getCumCasesDeathsPerCapita(dataLine):
    cases = int(dataLine[4])
    deaths = int(dataLine[5])
    population = int(dataLine[6])

    casesPerCapita = cases / population
    deathsPerCapita = deaths / population

    return [casesPerCapita, deathsPerCapita]


# GET: Pop, Cases, Deaths (per)
def getPopCasesDeathsPerMonth(dataLineList): # TODO: fix population part
    monthsDict = {}
    for dataLine in dataLineList:
        month = int(dataLine[2])
        cases = int(dataLine[4])
        deaths = int(dataLine[5])
        population = int(dataLine[6])
        if month not in monthsDict.keys():
            monthsDict[month] = [cases, deaths, population]
        else:
            monthsDict[month][0] += cases
            monthsDict[month][1] += deaths
            # monthsDict[month][2] = population

    return monthsDict

def getCountries(dict):
    countries = []
    for key in dict.keys():
        if key not in countries:
            countries += [key]
    return countries

# print(data.keys())
def printIntro():
    print("Welcome! Here you can acccess variation information related to global Covid-19 data. \n")
    print("Please select from the following options by inputting the corresponding number:")
    print("1. Display cumulative cases and deaths per continent")
    print("2. List a country's population, cases, and deaths per month")
    print("3. Perform stat analysis and save into an output data file")
    print("4. Display stat analysis results per continent")
    print("5. Visualize data for 3 countries based on your input (default is greece, china, us),starting on day of tenth death")
    print("6. Exit\n")


# Class for handling actions
class Response(object):
    def __init__(self, dataByCountry, dataByDate):
        self.dataByCountry = dataByCountry
        self.dataByDate = dataByDate
        self.actions = {
            1: self.menuOption1,
            2: self.menuOption2,
            3: self.menuOption3,
            4: "",
            5: "",
            6: "",
        }

    def respond(self, responseNum):
        return self.actions[responseNum]()

    def menuOption1(self):
        # DISPLAY CASES PER CONTINENT

        continents = ['Asia', 'America', 'Europe', 'Africa', 'Oceania']
        for continent in continents:
            total_cases = 0
            total_deaths = 0
            print(continent + ":", )
            for key in self.dataByCountry.keys():
                if key[1] == continent:
                    # Print a country's cases
                    # print(key[0]+": "+str(getTotalCases(data[key])))
                    total_cases += getTotalCasesFromCont(self.dataByCountry[key])
                    total_deaths += getTotalDeathsFromCont(self.dataByCountry[key])
            print("Total Cases: ", total_cases, )
            print("Total Deaths: ", total_deaths)
            print()
        print()

    def menuOption2(self):
        # LIST ONE COUNTRY'S POPULATION, CASES, DEATHS PER MONTH

        # Select a random country to display
        randomCountry = random.choice(getCountries(self.dataByCountry))
        # Print out the country's name
        print(randomCountry[0])
        print()
        # Get the country's monthly data on cases, deaths, and population
        months_dict = getPopCasesDeathsPerMonth(self.dataByCountry[randomCountry])
        # Display the data:
        table = []
        sortedMonthsDictKeys = sorted(months_dict.keys())
        # if december is in the months_dict, remove it from the end and add to the beginning
        if sortedMonthsDictKeys[-1] == 12:
            lastE = sortedMonthsDictKeys[-1:]
            sortedMonthsDictKeys = lastE+sortedMonthsDictKeys[:-1]
        # organize the data to be used in Tabulate
        for key in sortedMonthsDictKeys:
            tableData = [months[key]]+months_dict[key]
            table+=[tableData]
        print(tabulate(table, headers=['Month', 'Cases', 'Deaths', 'Population']))

    def menuOption3(self):
        # CREATE NEW FILE OF DATALINES THAT SHOW CUMULATIVE CASES, DEATHS AND AVG CASES, DEATHS PER CAPITA
        # partA_output_data = open("partA_output_data.txt", "x")
        partA_output_data = open("partA_output_data.txt", "w")
        newData = {}

        for country_cont in self.dataByCountry.keys():
            print(country_cont[0])
            entryNum = 1
            cumCases = 0
            cumDeaths = 0
            sumCasesPerCap = 0
            sumDeathsPerCap = 0
            for dataLine in self.dataByCountry[country_cont][::-1]: # reverse order to start from least recent
                if not dataLine[6].isdigit():
                    newDataLine = dataLine
                else:
                    cases = int(dataLine[4])
                    deaths = int(dataLine[5])
                    # Address cumulative cases,deaths
                    cumCases += cases
                    cumDeaths += deaths
                    # get current cases and deaths per capita
                    casesPerCapita,deathsPerCapita = getCumCasesDeathsPerCapita(dataLine)
                    # Address sum of average cases,deaths per capita
                    sumCasesPerCap += casesPerCapita
                    sumDeathsPerCap += deathsPerCapita
                    # create the new Line
                    # newDataLine = date, day, month, year, cumCases, cumDeaths, avgCasesPerCap, avgDeathsPerCap, country, continent
                    newDataLine = [dataLine[0], dataLine[1], dataLine[2], dataLine[3], str(cumCases), str(cumDeaths),
                                   str(sumCasesPerCap/entryNum)[:4], str(sumDeathsPerCap/entryNum)[:4], country_cont[0], country_cont[1]]
                if country_cont not in newData.keys():
                    newData[country_cont] = [newDataLine]
                else:
                    newData[country_cont].append(newDataLine)

                # all done, increment entryNum
                entryNum += 1
        # Add newData to new file
        partA_output_data.write("date, day, month, year, cumCases, cumDeaths, avgCasesPerCap, avgDeathsPerCap, country, continent \n")
        for country_cont in newData.keys():
            for dataLine in newData[country_cont][::-1]: # reverse to start from most recent
                partA_output_data.write(", ".join(dataLine))
                partA_output_data.write("\n")
        partA_output_data.close()
        # cumulative cases: each line, add cases to a total, display total on each subsequent line
        # cum deaths: each line, add deaths to a total, display total on each subsequent line
        # avg cases per cap: keep track of entry number, calc cases per cap, add to
        

def main():
    dataByCountry, dataByDate = organize_file_data()
    # printIntro()


    MyResponse = Response(dataByCountry, dataByDate)
    while True:
        userInput = input("Enter your selection:")

        if not userInput.isdigit():
            print("ERROR: input must be a number!")
        else:
            number = int(userInput)
            if 0 < number <= 6:  # Display cases and deaths per continent
                print()
                MyResponse.respond(number)
                print()
            else:
                print("ERROR: the number must be between 1 and 6!")


main()
