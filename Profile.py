class Profile:

    def __init__(self, username: str, password: str, balance: int, wins: int, losses: int, buy_in: int):
        self.username = username
        self.password = password

        self.balance = balance
        self.wins = wins
        self.losses = losses
        self.buy_in = buy_in

    def add_money(self, amount: int):
        self.balance += amount
        self.buy_in += amount

    # Removes money from the account and from total buy in
    def remove_money(self, amount: int):
        self.balance -= amount
        self.buy_in -= amount

    def get_balance(self):
        return self.balance

    def update_balance(self, balance: int):
        self.balance = balance

    def print_stats(self):
        print("Current Balance: $" + str(self.balance))
        print("Total Wins:", self.wins)
        print("Total Losses:", self.losses)
        print("Buy in amount: $" + str(self.buy_in), '\n')

