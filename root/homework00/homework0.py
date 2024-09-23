# assert constants
PEOPLE_PER_LARGE = 7
PEOPLE_PER_MEDIUM = 3
PEOPLE_PER_SMALL = 1
DIAMETER_LARGE = 20
DIAMETER_MEDIUM = 16
DIAMETER_SMALL = 12
COST_LARGE = 14.68
COST_MEDIUM = 11.48
COST_SMALL = 7.28
PI = 3.14159265

def countYourManyPizzas(people):
    # calculate large pizzas
    countLarge = people // PEOPLE_PER_LARGE
    # calculate medium pizzas using the remaining number of people after large pizzas
    countMedium = (people % PEOPLE_PER_LARGE) // PEOPLE_PER_MEDIUM
    # # calculate small pizzas using the remaining number of people after large and medium pizzas
    countSmall = ((people % PEOPLE_PER_LARGE) % PEOPLE_PER_MEDIUM) // PEOPLE_PER_SMALL
    if (((people % PEOPLE_PER_LARGE) % PEOPLE_PER_MEDIUM) % PEOPLE_PER_SMALL) > 0:
        countSmall += 1
    print(f"{countLarge} large pizzas, {countMedium} medium pizzas, and {countSmall} small pizzas will be needed.")
    return countLarge, countMedium, countSmall

# calculate area of each pizza and then sum the total area of pizzas
def servingSize(people, countLarge, countMedium, countSmall):
    largePizzaArea = (((1/2) * DIAMETER_LARGE)**2) * PI
    mediumPizzaArea = (((1/2) * DIAMETER_MEDIUM)**2) * PI
    smallPizzaArea = (((1/2) * DIAMETER_SMALL)**2)  * PI
    totalPizzaArea = (countLarge * largePizzaArea) + (countMedium* mediumPizzaArea) + (countSmall * smallPizzaArea)
    totalPizzaAreaPerGuest = (totalPizzaArea / people)
    print(f"A total of {totalPizzaArea:.2f} square inches of pizza will be ordered ({totalPizzaAreaPerGuest:.2f} per guest).")

# calculate the total cost and then add a tip based off of a percentage
def payingThePiper(tip, countLarge, countMedium, countSmall):
    cost = (countLarge * COST_LARGE) + (countMedium * COST_MEDIUM) + (countSmall * COST_SMALL)
    totalCost = cost + (cost * tip)
    print(f"The total cost of the event will be: ${totalCost:.2f}.")

def main():
    # get number of people
    people = int(input(f"Please enter how many guests to order for:"))
    countLarge, countMedium, countSmall = countYourManyPizzas(people)
    print()
    servingSize(people, countLarge, countMedium, countSmall)
    # get the tip percentage
    tip = float(input(f"Please enter the tip as a percentage (i.e. 10 means 10%):")) / 100
    payingThePiper(tip, countLarge, countMedium, countSmall)
    print()

if __name__ == "__main__":
    main()
