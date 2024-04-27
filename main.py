import random


MAX_LINES = 3
MAX_BET = 100
MIN_BET = 1

ROWS = 3
COLS = 3


jackpot = 0
contribution_percentage = 0.01
free_spins_multiplier = 2
bonus_round_multiplier = 3

symbol_count = {
    "1": 2,
    "2": 4,
    "3": 6,
    "4": 8
}

symbol_values = {
    "1": 5,
    "2": 4,
    "3": 3,
    "4": 2
}

def check_winnings(columns, lines, bet, values):
    winnings = 0
    winning_lines = []
    for line in range(lines):
        symbol = columns[0][line]
        for column in columns:
            symbol_to_check = column[line]
            if symbol != symbol_to_check:
                break
        else:
            winnings += values[symbol] * bet
            winning_lines.append(line + 1)

    return winnings, winning_lines



def get_slot_machine_spin(rows, cols, symbols):
    all_symbols = []
    for symbol, symbol_count in symbols.items():
        for _ in range(symbol_count):
            all_symbols.append(symbol)

    columns = []
    for _ in range(cols):
        column = []
        current_symbols = all_symbols[:]
        for _ in range(rows):
            value = random.choice(current_symbols)
            current_symbols.remove(value)
            column.append(value)

        columns.append(column)

    return columns


def print_slot_machine(columns):
    for row in range(len(columns[0])):
        for i, column in enumerate(columns):
            if i != len(columns) - 1:
                print(column[row], end=" |")
            else:
                print(column[row], end="")
        print()


def deposit():
    while True:
        amount = input("Enter the amount you want to deposite: $")
        if amount.isdigit():
            amount = int(amount)
            if amount > 0:
                break
            elif amount < 0:
                print("Quitting the game...")
                exit()
            else:
                print("Invalid amount. Please enter a valid amount greater than 0.")
        else:
            print(" Please enter a number.")
    return amount

def get_number_of_lines():
    while True:
        lines = input("Enter the number of lines to bet on )1-" + str(MAX_LINES) + ")? ")
        if lines.isdigit():
            lines = int(lines)
            if 1 <= lines <= MAX_LINES:
                break
            else:
                print("Invalid number of lines. Please enter a valid number of lines.")
        else:
            print("Please enter a number.")
    return lines

def get_bet():
    while True:
        amount = input("What would you like to bet on each line?: $")
        if amount.isdigit():
            amount = int(amount)
            if MIN_BET <= amount <= MAX_BET:
                break
            else:
                print(f"Amount must be between ${MIN_BET} - ${MAX_BET}. Please enter a valid amount.")
        else:
            print(" Please enter a number.")
    return amount

def spin(balance):
    global jackpot

    lines = get_number_of_lines()
    bet = get_bet()
    total_bet = bet * lines

    if random.random() < contribution_percentage:
        jackpot += total_bet

    print(f"You are betting ${bet} on {lines}. Total bet is equal to: ${total_bet} ")

    slots = get_slot_machine_spin(ROWS, COLS, symbol_count)
    print_slot_machine(slots)

    winnings, winning_lines = check_winnings(slots, lines, bet, symbol_values)

    # Check for free spins
    if slots[0][0] == slots[1][0] == slots[2][0] == "1":
        print("Congratulations, you've triggered free spins!")
        free_spins_winnings = 0
        for _ in range(5):
            free_spins_slots = get_slot_machine_spin(ROWS, COLS, symbol_count)
            free_spins_winnings += check_winnings(free_spins_slots, lines, bet, symbol_values)[0]
        winnings += free_spins_winnings * free_spins_multiplier
        print(f"You won ${free_spins_winnings * free_spins_multiplier} in free spins!")

    # Check for bonus round
    if slots[0][1] == slots[1][1] == slots[2][1] == "2":
        print("Congratulations, you've triggered the bonus round!")
        bonus_round_winnings = 0
        for _ in range(3):
            bonus_round_slots = get_slot_machine_spin(ROWS, COLS, symbol_count)
            bonus_round_winnings += check_winnings(bonus_round_slots, lines, bet, symbol_values)[0]
        winnings += bonus_round_winnings * bonus_round_multiplier
        print(f"You won ${bonus_round_winnings * bonus_round_multiplier} in the bonus round!")

    # Check for jackpot
    if winning_lines == [3]:
        winnings *= 10 # 10x multiplier for getting the rarest combination on the third payline
        jackpot -= winnings # subtract the jackpot amount from the jackpot pool
        print(f"Congratulations, you've won the jackpot! ${winnings}")

    print(f"You won ${winnings}!")
    print(f"You won on lines:", * winning_lines)

    return winnings - total_bet


def main():
    balance = deposit()
    while True:
        if balance <= 0:
            print("You have run out of balance. Please deposit more money to continue playing.")
            balance = deposit()
            continue

        print(f"Your current balance is: ${balance}")
        answer = input(" Press enter to play (q to quit).")
        if answer == "q":
            break
        winnings = spin(balance)
        balance += winnings

    print(f"You left with ${balance}. Thank you for playing!")


main()