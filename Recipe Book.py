import random
import streamlit as st
from collections import defaultdict

# Cataloging the dinner recipes
recipeDinner = {"Burrito":["Refried Beans", "Tortillas", "Mexican Cheese", "Rice"],
                "Tilapia":["Tilapia", "Green Beans", "Couscous"],
                "Chickpea Curry":["Chickpeas", "Rice", "Curry Sauce"],
                "Grilled Cheese":["Bread", "American Cheese", "Tomato Soup"],
                "Cauliflower Skillet":["Cauliflower", "Mushrooms", "Tofu"],
                "Sausage Skillet":["White Beans", "White Beans", "Smoked Sausage", "Spinach"],
                "Fried Rice": ["Rice", "Veggies"],
                "Vodka Pasta": ["Tomato Paste", "Heavy Cream"]}

# Creating a randomly generated list
days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"]


# Creating the grocery list
def grocer(randPlan):
    from collections import defaultdict

    grocList = []
    for x in randPlan.values():
        if x in recipeDinner:
            grocList.append(recipeDinner[x])

    flat = [item for sublist in grocList for item in sublist]

    counts = defaultdict(int)
    for item in flat:
        counts[item] += 1

    result = []
    seen_blocklist = set()
    blocklist = {"Bread", "Tortillas", "Rice"}

    for item in counts:
        if item in blocklist:
            # just add once, no count prefix
            result.append(item)
        else:
            count = counts[item]
            if count == 1:
                result.append(item)
            else:
                result.append(f"{count}x {item}")

    return result

# User Sided

def main():
    print("Select an option:\n 1. View recipe book\n 2. Randomly generate weekly plan\n 3. Manually create weekly plan")
    while True:
        user_input = input("You: ")
        if user_input.lower() == "exit":
            print("Goodbye!")
            break
        elif user_input.lower() == "1":
            for item in list(recipeDinner.keys()):
                print(item)
        elif user_input.lower() == "2":
            while True:
                keys = list(recipeDinner.keys())
                random.shuffle(keys)
                randPlan = {}
                for x in range(len(days)):
                    randPlan[days[x]] = keys[x]
                for key, value in randPlan.items():
                    print(f"{key}: {value}\n")
                print("Would you like to rerandomize the plan, edit the plan, or generate a grocery list?"
                      "\n 1. Rerandomize\n 2. Edit\n 3. Generate")
                user_input = input("You: ")
                if user_input.lower() == "1":
                    continue
                if user_input.lower() == "2":
                    while True:
                        print("Which day(s) would you like to change?")
                        user_input = input("You: ")
                        dayChange = [item.strip() for item in user_input.split(",")]
                        for day in dayChange:
                            print(f"What would you like to have on {day} instead?")
                            user_input = input("You: ")
                            if user_input in list(recipeDinner.keys()):
                                randPlan[day] = user_input
                        for key, value in randPlan.items():
                            print(f"{key}: {value}\n")
                        print("Is that right? \n1. Yes\n2. No")
                        user_input = input("You: ")
                        if user_input.lower() == "1":
                            grocList = grocer(randPlan)
                            print("Here is the grocery list:")
                            for item in list(grocList):
                                print(item)
                            return
                        if user_input.lower() == "2":
                            continue
                if user_input.lower() == "3":
                    grocList = grocer(randPlan)
                    print("Here is the grocery list:")
                    for item in list(grocList):
                        print(item)
                    return
        elif user_input.lower() == "3":
            manPlan = {}
            for day in days:
                print(f"What would you like to have on {day}")
                user_input = input("You: ")
                if user_input in list(recipeDinner.keys()):
                    manPlan[day] = user_input
            for key, value in manPlan.items():
                print(f"{key}: {value}\n")
            print("Is that right? \n1. Yes\n2. No")
            user_input = input("You: ")
            if user_input.lower() == "1":
                grocList = grocer(manPlan)
                print("Here is the grocery list:")
                for item in list(grocList):
                    print(item)
                return
            while True:
                if user_input.lower() == "2":
                    print("Which day(s) would you like to change?")
                    user_input = input("You: ")
                    dayChange = [item.strip() for item in user_input.split(",")]
                    for day in dayChange:
                        print(f"What would you like to have on {day} instead?")
                        user_input = input("You: ")
                        if user_input in list(recipeDinner.keys()):
                            manPlan[day] = user_input
                    for key, value in manPlan.items():
                        print(f"{key}: {value}\n")
                    print("Is that right? \n1. Yes\n2. No")
                    user_input = input("You: ")
                    if user_input.lower() == "1":
                        grocList = grocer(manPlan)
                        print("Here is the grocery list:")
                        for item in list(grocList):
                            print(item)
                        return
                    if user_input.lower() == "2":
                        continue




if __name__ == "__main__":
    main()


