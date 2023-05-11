class Category:
    def __init__(self, name):
        self.name = name
        self.ledger = list()
        self.balance = float()

    def __str__(self):
        # Override the super method for when printing out the object
        # Returns ledger list
        print_ledger = str()
        print_ledger += f"{self.name.center(30, '*')}\n"

        for item in self.ledger:
            print_ledger += f"{item['description'][:23].ljust(23)}{('{:.2f}'.format(item['amount'])).rjust(7)}\n"

        print_ledger += f"Total: {self.balance}"

        return print_ledger

    def deposit(self, amount, description=""):
        # add amount to balance and ledger
        self.balance += amount
        self.ledger.append({
            "amount": amount,
            "description": description
        })

    def withdraw(self, amount, description=""):
        # subtract amount from balance and add negative amount to ledger
        # Returns success boolean
        if self.check_funds(amount):
            self.balance -= amount
            self.ledger.append({
                "amount": -amount,
                "description": description
            })
            return True
        else:
            return False

    def get_balance(self):
        return self.balance

    def transfer(self, amount, category):
        # move amount from one category to another if there are enough funds
        # Returns success boolean
        if self.check_funds(amount):
            self.withdraw(amount, f"Transfer to {category.name}")
            category.deposit(amount, f"Transfer from {self.name}")
            return True
        else:
            return False

    def check_funds(self, amount):
        # Returns boolean if there is enough money in balance
        if amount > self.balance:
            return False
        else:
            return True


def create_spend_chart(categories):
    # Returns bar graph of percentage spent per category
    if len(categories) > 4:
        print("Max 4 categories")
    else:
        percentage_per_category = dict()

        for category in categories:
            # List comprehension of getting the total withdrawals and deposits per category
            total_withdrawals = sum(abs(item['amount']) for item in category.ledger if item['amount'] < 0)
            total_deposits = sum(abs(item['amount']) for item in category.ledger if item['amount'] > 0)

            # Calculate percentage spent on each category and add it to a dictionary
            percentage_spent = (total_withdrawals / total_deposits) * 100
            percentage_per_category[category.name] = percentage_spent

        # Building the bar chat
        bar_chart = str()
        bar_chart += f"Percentage spent by category\n"
        percentage_max = 100

        # Building the bar percentage
        while percentage_max > -1:
            bar_chart += f"{str(percentage_max).rjust(3)}|"

            for name, percentage in percentage_per_category.items():
                if percentage >= percentage_max:
                    bar_chart += " o "
                else:
                    bar_chart += "   "

            percentage_max -= 10
            bar_chart += " \n"

        bar_chart += f"    {''.ljust(3 * len(categories) + 1, '-')}"

        # Building the vertical category names
        for i in range(0, max([len(category.name) for category in categories])):
            bar_chart += "\n    "
            for category in categories:
                if len(category.name) > i:
                    bar_chart += f" {category.name[i]} "
                else:
                    bar_chart += "   "
            bar_chart += " "

        return bar_chart
