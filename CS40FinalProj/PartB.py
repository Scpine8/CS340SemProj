# Final Project Part B
#
# Licensed under the GNU Open Source License agreement.
#
# Sean Pine 06/6/20 20190377@student.act.edu


# Artificial Neural Network

class Response(object): # Strategy Design Pattern
    def __init__(self):
        self.actions = {
            1: self.enterNetworkTopology,
            2: self.initiateATrainingPass,
            3: self.classifyTestData,
            4: self.displayTrainingResultGraphics
        }

    def respond(self, responseNum):
        return self.actions[responseNum]()

    def enterNetworkTopology(self):
        pass

    def initiateATrainingPass(self):
        pass

    def classifyTestData(self):
        pass

    def displayTrainingResultGraphics(self):
        pass


def main():
    MyResponse = Response()
    while True:
        userInput = input("Enter your selection:")

        if not userInput.isdigit():
            print("ERROR: input must be a number!")
        else:
            number = int(userInput)
            if 0 < number < 5:  # Display cases and deaths per continent
                print()
                MyResponse.respond(number)
                print()
            elif number == 5:
                break
            else:
                print("ERROR: the number must be between 1 and 6!")