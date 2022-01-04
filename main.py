from Card import Card
import random
from Profile import Profile

# Global variable for profile data
all_profile_data: dict[str: Profile]


# Loads the Profile_data.csv file, and reads the data into a global dictionary variable
# where the key is the username and the value is a profile data type containing their information
def load_profiles():
    profile_data = {}
    f = open("Profile_data.csv", 'r')

    for line in f.readlines():

        if line == "\n":
            continue

        text_data = line.replace("\n", "").split(',')

        username = text_data[0]
        password = text_data[1]
        stats = []

        for i in range(2, 6):
            stats.append(int(text_data[i]))

        temp: Profile = Profile(username, password, *stats)
        profile_data[username] = temp

    return profile_data


def update_file(profile):

    file = open("Profile_data.csv", "r+")
    all_profile_data[profile.username] = profile

    for name in all_profile_data:
        file.write(name + ',' + all_profile_data[name].password + ',' + str(all_profile_data.get(name).balance) + ',' +
                   str(all_profile_data.get(name).wins) + ',' + str(all_profile_data.get(name).losses) + ',' +
                   str(all_profile_data.get(name).buy_in) + ',\n')

    file.close()


def sign_in():

    print("Signing In")
    username: str = input("Enter your Username: ").lower()
    password: str = input("Enter your Password: ")

    # Will prompt the user until a valid username:password combo is entered
    if username not in all_profile_data or (username in all_profile_data and password != all_profile_data[username].password):
        print("Incorrect username or password, try again.")
        username = input("Enter your Username: ").lower()
        password = input("Enter your Password: ")

    return all_profile_data.get(username)


# If the user does not have an account, they will create a new one here and the data will be saved
# to Profile_data.csv.  Then the new profile will be returned so the user can start playing
def create_acct():

    print("Creating Account")
    empty = [0, 0, 0, 0]
    username = input("Enter your Username: ").lower()

    while username in all_profile_data:
        print("Username already in use, try again")
        username = input("Enter your Username: ").lower()

    password: str = input("Enter your Password: ")
    new_profile = Profile(username, password, *empty)
    update_file(new_profile)

    return new_profile


# Get the card values and order them into groups of each persons hand, and the table cards
def get_cards():
    all_cards = {}
    index = 0
    file = open('Cards.csv', 'r')

    for line in file.readlines():
        split = line.split(',')
        all_cards[index] = Card(split[0], int(split[1]), int(split[2]))
        index += 1

    dealt = []
    i = 0

    while len(dealt) < 9:
        rand_card = random.randint(0, 51)

        while all_cards[rand_card] in dealt:
            rand_card = random.randint(0, 51)

        dealt.append(all_cards[rand_card])
        i += 1

    table: list[Card] = [dealt[0], dealt[1], dealt[2], dealt[3], dealt[4]]
    user_hand: list[Card] = [dealt[5], dealt[6]]
    house_hand: list[Card] = [dealt[7], dealt[8]]

    # For testing specific hands
    """table: list[Card] = [
        Card("Temp 1", 4, 1),
        Card("Temp 2", 3, 1),
        Card("Temp 3", 9, 1),
        Card("Temp 4", 5, 1),
        Card("Temp 5", 6, 1)]

    user_hand: list[Card] = [
        Card("Temp 6", 14, 1),
        Card("Temp 7", 2, 4)]

    house_hand: list[Card] = [
        Card("Temp 8", 12, 4),
        Card("Temp 9", 2, 4)]"""

    return table, user_hand, house_hand


# Sorts the hand and table cards into descending order
def sort(table, hand):
    cards = table + hand
    ordered = []
    i = 0

    # Takes the table and pocket cards, and returns them in an ordered list of descending values
    for card in cards:

        for curr in ordered:
            if curr.value < card.value:
                break

            i += 1

        if card.value != 0:
            ordered.insert(i, card)
            i = 0

    return ordered


# Checks if a Royal Flush was hit
def is_royal(table, hand):
    showdown = is_straight(table, hand)

    # If a Royal Flush was hit, set the value to 10 to represent it
    if showdown >= 9.14:
        return 10

    return 0


# Checks if a Straight Flush was hit
# is_straight() returns a value for a straight or straight flush. This function is responsible for
# classifying the output appropriately
def is_straight_flush(table, hand):
    showdown = is_straight(table, hand)
    if 9 < showdown < 9.14:
        return showdown

    return 0


# Checks if a Four-of-a-Kind was hit
def is_four(table, hand):
    showdown = 0
    ordered = sort(table, hand)

    for i in range(len(ordered) - 3):

        count = 1

        for j in range(3):

            if ordered[i].value == ordered[i + j + 1].value:
                count += 1

        # Get showdown value if a Three of a Kind is found
        if count == 4:

            div = 100

            showdown = 8 + ordered[i].value / div
            showdown += ordered[i].value / pow(div, 2)
            showdown += ordered[i].value / pow(div, 3)
            showdown += ordered[i].value / pow(div, 4)

            for k in range(5):

                if ordered[k].value != ordered[i].value:
                    showdown += ordered[k].value / pow(div, 5)
                    break

    return showdown


# Checks is a Full House was hit
def is_full_house(table, hand):
    ordered = sort(table, hand)
    pair = 0
    showdown = 0
    tripp = is_three(table, hand) - 4

    if tripp <= 0:
        return 0

    tripp: int = int(tripp * 100)

    for i in range(len(ordered)):

        if ordered[i].value != tripp:
            cmp = ordered[i].value

            # Compare each value after cmp with cmp to see if they match
            for k in range(len(ordered) - i - 1):

                if cmp == ordered[i + k + 1].value and cmp > pair:

                    pair = cmp

                    temp_showdown = 7 + tripp / 100
                    temp_showdown += tripp / pow(100, 2)
                    temp_showdown += tripp / pow(100, 3)
                    temp_showdown += pair / pow(100, 4)
                    temp_showdown += pair / pow(100, 5)

                    if temp_showdown > showdown:
                        showdown = temp_showdown

    return showdown


# Checks if a Flush was hit
def is_flush(table, hand):
    num_hearts = 0
    num_spades = 0
    num_clubs = 0
    num_diamonds = 0
    showdown = 0
    suit = 0

    ordered = sort(table, hand)

    for i in range(len(ordered)):

        # Count the total occurrences of each suit
        if ordered[i].suit == 1:
            num_hearts += 1

        elif ordered[i].suit == 2:
            num_spades += 1

        elif ordered[i].suit == 3:
            num_clubs += 1

        elif ordered[i].suit == 4:
            num_diamonds += 1

        # Checks if a flush has been hit, and if so, determine the suit
        if num_hearts == 5:
            suit = 1

        elif num_spades == 5:
            suit = 2

        elif num_diamonds == 5:
            suit = 3

        elif num_clubs == 5:
            suit = 4

    if suit != 0:

        showdown = 6
        exp = 1

        for i in range(len(ordered)):

            if ordered[i].suit == suit:
                showdown += ordered[i].value / pow(100, exp)
                exp += 1

    return showdown


# Checks if a Straight or Straight Flush was hit
def is_straight(table, hand):
    num_hearts = 0
    num_spades = 0
    num_clubs = 0
    num_diamonds = 0

    showdown = 0

    ordered = sort(table, hand)

    for i in range(len(ordered) - 4):

        # In case of consecutive numbers, skip and continue checking for straight
        skip = 0

        for j in range(len(ordered) - i):

            # Statements to check if a straight exists
            if ordered[i + j].value == ordered[i + j - 1].value:
                skip += 1

            elif ordered[i + j].value != ordered[i].value - j + skip:
                break

            # Runs if a straight is hit
            elif (ordered[i + j].value == ordered[i].value - j + skip) and (j == 4 + skip):

                high = ordered[i].value
                temp_showdown = 5 + (high / 100)

                # Checks if the straight is also a flush
                for k in range(i, i + j):

                    if ordered[k].suit == 1:
                        num_hearts += 1

                    elif ordered[k].suit == 2:
                        num_spades += 1

                    elif ordered[k].suit == 3:
                        num_clubs += 1

                    elif ordered[k].suit == 4:
                        num_diamonds += 1

                if (num_hearts >= 5) or (num_spades >= 5) or (num_clubs >= 5) or (num_diamonds >= 5):
                    flush = True
                    temp_showdown += 4

                if temp_showdown > showdown:
                    showdown = temp_showdown

    return showdown


# Checks if a Three of a Kind was hit
def is_three(table, hand):
    showdown = 0
    ordered = sort(table, hand)

    for i in range(len(ordered) - 2):

        count = 1

        for j in range(2):

            if ordered[i + j + 1].value == ordered[i].value:
                count += 1

        # Get showdown value if a three of a kind is found
        if count == 3:

            exp = 4

            temp_showdown = 4 + ordered[i].value / 100
            temp_showdown += ordered[i].value / pow(100, 2)
            temp_showdown += ordered[i].value / pow(100, 3)

            for k in range(5):

                if ordered[k].value != ordered[i].value:
                    temp_showdown += ordered[k].value / pow(100, exp)
                    exp += 1

                if exp == 6:
                    break

            if temp_showdown > showdown:
                showdown = temp_showdown

    return showdown


# Checks if a Two Pair was hit
def is_two_pair(table, hand):
    showdown = 0
    pair_two = 0

    ordered = sort(table, hand)
    pair_one = is_pair(table, hand) - 2

    if pair_one <= 0:
        return 0

    pair_one: int = int(pair_one * 100)

    for i in range(len(ordered) - 1):

        if ordered[i].value != pair_one and ordered[i].value == ordered[i + 1].value:
            pair_two = ordered[i].value

    if pair_two > 0:

        showdown = 3
        showdown += pair_one / pow(100, 1)
        showdown += pair_one / pow(100, 2)
        showdown += pair_two / pow(100, 3)
        showdown += pair_two / pow(100, 4)

        for i in range(len(ordered)):

            if ordered[i].value != pair_one and ordered[i].value != pair_two:
                showdown += ordered[i].value / pow(100, 5)
                break

    return showdown


# Checks if a Pair was hit
def is_pair(table, hand):
    showdown = 0
    ordered = sort(table, hand)

    for i in range(len(ordered) - 1):

        if ordered[i].value == ordered[i + 1].value:

            temp_showdown = 2 + ordered[i].value / 100
            temp_showdown += ordered[i].value / pow(100, 2)

            exp = 3

            for j in range(5):

                if ordered[j].value != ordered[i].value:
                    temp_showdown += ordered[j].value / pow(100, exp)
                    exp += 1

                if exp == 6:
                    break

            if temp_showdown > showdown:
                showdown = temp_showdown

    return showdown


# Returns the 5 highest card values in order
def get_high(table, hand):
    ordered = sort(table, hand)
    showdown = 1
    divisor = 100

    for i in ordered:
        showdown += i.value / divisor
        divisor *= 100

    return showdown


# Gets the value of a hand to compare with the other hands value
# Values stored by a value representing hand strength, followed by
# a decimal of the hand with the most important values coming first
def get_showdown(table, hand):
    """
        10 - Royal Flush
        9 - Straight Flush
        8 - Four of a Kind
        7 - Full House
        6 - Flush
        5 - Straight
        4 - Three of a kind
        3 - Two Pair
        2 - Pair
        1 - High Card
    """

    # Default showdown as high card
    showdown = 0

    # Checks for best hands first until one is found

    # Royal Flush
    if showdown < is_royal(table, hand):
        showdown = is_royal(table, hand)
        name = "Royal Flush"

    # Straight Flush
    elif showdown < is_straight_flush(table, hand):
        showdown = is_straight_flush(table, hand)
        name = "Straight Flush"

    # Four of a Kind
    elif showdown < is_four(table, hand):
        showdown = is_four(table, hand)
        name = "Four of a Kind"

    # Full House
    elif showdown < is_full_house(table, hand):
        showdown = is_full_house(table, hand)
        name = "Full House"

    # Flush
    elif showdown < is_flush(table, hand):
        showdown = is_flush(table, hand)
        name = "Flush"

    # Straight
    elif showdown < is_straight(table, hand):
        showdown = is_straight(table, hand)
        name = "Straight"

    # Three of a Kind
    elif showdown < is_three(table, hand):
        showdown = is_three(table, hand)
        name = "Three of a Kind"

    # Two Pair
    elif showdown < is_two_pair(table, hand):
        showdown = is_two_pair(table, hand)
        name = "Two Pair"

    # Pair
    elif showdown < is_pair(table, hand):
        showdown = is_pair(table, hand)
        name = "Pair"

    # High Card
    else:
        showdown = get_high(table, hand)
        name = "High Card"

    # Returns 10 decimal values to represent the values of the 5 showdown cards in order of importance
    return round(showdown, 10), name


# Allows the user to play against the computer
def play(profile: Profile):

    stop_bool = False
    balance = profile.balance
    print('\033[1m' + '\033[4m' + "\nStats:" + '\033[0m')
    profile.print_stats()

    if balance == 0:
        balance = int(input("Balance is 0, add money: $"))
        profile.add_money(balance)
        update_file(profile)

    print("After each round, enter 'q' to quit or hit enter to play another round")
    ante = int(input("Enter desired ante amount: $"))

    while not stop_bool:

        while balance < 3 * ante:
            add_funds = input("Not enough money, add more? (y/n): ")

            if add_funds == "y":
                add_amount = int(input("Amount: $"))
                profile.add_money(add_amount)
                update_file(profile)
                balance += add_amount

            else:
                return profile

        table, user_hand, house_hand = get_cards()
        print("-------------------------------------------------------------------------------------------------------")
        print('\033[1m' + '\033[4m' + "Hand:" + '\033[0m', user_hand[0].name, "\\", user_hand[1].name)
        print('\033[1m' + '\033[4m' + "Flop:" + '\033[0m', table[0].name, "\\", table[1].name, "\\", table[2].name)
        balance -= ante

        if input("Call 2x ante bet? (y/n): ") == 'y':

            print("")
            balance -= 2 * ante
            # all cards are shown so determine the winner.  House has to have pair of 4 or better

            print('\033[1m' + '\033[4m' + "User Hand:" + '\033[0m', user_hand[0].name, "\\", user_hand[1].name)
            print('\033[1m' + '\033[4m' + "House Hand:" + '\033[0m', house_hand[0].name, "\\", house_hand[1].name)
            print('\033[1m' + '\033[4m' + "Turn/River:" + '\033[0m', table[0].name, "\\", table[1].name, "\\",
                  table[2].name, "\\", table[3].name, "\\",
                  table[4].name)

            user_showdown, user_showdown_name = get_showdown(table, user_hand)
            house_showdown, house_showdown_name = get_showdown(table, house_hand)

            # Checks if the house has a better hand than a pair of 4's
            if house_showdown < 2.0404:
                print('\033[1m' + '\033[4m' + "--House did not qualify; Draw--\n" + '\033[0m')
                balance += 3 * ante

            elif user_showdown > house_showdown:
                print('\033[1m' + '\033[4m' + "--User Wins with " + user_showdown_name + "--\n" + '\033[0m')
                balance += 6 * ante
                profile.wins += 1

            elif house_showdown > user_showdown:
                print('\033[1m' + '\033[4m' + "--House Wins with " + house_showdown_name + "--\n" + '\033[0m')
                profile.losses += 1

            else:
                print('\033[1m' + '\033[4m' + "--Draw--\n" + '\033[0m')

        print('\033[1m' + '\033[4m' + "Balance: $" + '\033[0m', balance)
        print("-------------------------------------------------------------------------------------------------------")

        if balance <= 0:
            continue

        stop = input("'Enter' to play again, 'q' to quit:")
        if stop == "q":
            print(
                "-------------------------------------------------------------------------------------------------------")

            profile.update_balance(balance)
            update_file(profile)
            return profile

    return profile


# Main
def main():

    print("Welcome to Caribbean Poker")
    print("Do you have an existing profile?")
    returning_user = input("Y/N ").lower()

    if returning_user == 'y':
        curr_profile: Profile = sign_in()

    elif returning_user == 'n':
        curr_profile: Profile = create_acct()

    else:
        print("Not an option, redirecting you to profile creation...")
        curr_profile: Profile = create_acct()

    curr_profile = play(curr_profile)
    curr_profile.print_stats()
    print("Thanks for playing!")


all_profile_data = load_profiles()
main()


"""
TODO

- Add the 100:1 for royal flush and other side pots

"""