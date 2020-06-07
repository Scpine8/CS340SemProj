# Main Menu Options

"""
1. Display cumulative cases and deaths per continent
2. List a country's population, cases, and deaths per month
3. Perform stat analysis and save into an output data file
4. Display stat analysis results per continent
5. Visualize data for 3 countries based on user input (default is greece, china, us),
starting on day of tenth death
6. Exit the program

"""

import random

# First, import a csv


def organize_file_data():
    line1 = True
    inputStream = open("partA_input_data.txt")

    data = {}

    for line in inputStream:
        if not line1:
            lineSplit = line.split(',')  # split the line into an array of values
            date, day, month, year = lineSplit[0], lineSplit[1], lineSplit[2], lineSplit[3]
            cases, deaths, country, population, continent = lineSplit[4], lineSplit[5], lineSplit[6], lineSplit[9], \
                                                            lineSplit[10]
            country_cont = (country, continent[:-1]) # country is parsed to erase automatic line break
            country_cont_data = [date, day, month, year, cases, deaths, population]

            if country_cont not in data.keys():
                data[country_cont] = [country_cont_data]
            else:
                data[country_cont].append(country_cont_data)
        else:
            line1 = False
    return data


def getTotalCasesFromCont(dataLineList):
    cases = 0
    for dataline in dataLineList:
        cases += int(dataline[4])
    # print("Cases: " + str(cases))
    return cases


def getTotalDeathsFromCont(dataLineList):
    deaths = 0
    for dataline in dataLineList:
        deaths += int(dataline[5])
    # print("Deaths: " + str(deaths))
    return deaths

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
    print(
        "5. Visualize data for 3 countries based on your input (default is greece, china, us),starting on day of tenth death")
    print("6. Exit\n")


# Class for handling actions
class Response(object):
    def __init__(self, dataDict):
        self.data = dataDict
        self.actions = {
            1: self.DisplayCasesDeathsPerCont,
            2: self.ListOneCountryPopCasesDeathsPerMonth,
            3: "",
            4: "",
            5: "",
            6: "",
        }

    def respond(self, responseNum):
        return self.actions[responseNum]()

    def DisplayCasesDeathsPerCont(self):
        continents = ['Asia', 'America', 'Europe', 'Africa', 'Oceania']
        for continent in continents:
            total_cases = 0
            total_deaths = 0
            print(continent + ":", )
            for key in self.data.keys():
                if key[1] == continent:
                    # Print a country's cases
                    # print(key[0]+": "+str(getTotalCases(data[key])))
                    total_cases += getTotalCasesFromCont(self.data[key])
                    total_deaths += getTotalDeathsFromCont(self.data[key])
            print("Total Cases: ", total_cases, )
            print("Total Deaths: ", total_deaths)
            print()
        print()

    def ListOneCountryPopCasesDeathsPerMonth(self):
        print(getCountries(self.data))
        print(random.choice(getCountries(self.data)))

def main():
    data = organize_file_data()
    printIntro()

    MyResponse = Response(data)
    while True:
        userInput = input("Enter here:")

        if not userInput.isdigit():
            print("ERROR: input must be a number!")
        else:
            number = int(userInput)
            if 0 < number <= 6:  # Display cases and deaths per continent
                print()
                MyResponse.respond(number)
            else:
                print("ERROR: the number must be between 1 and 6!")


main()
