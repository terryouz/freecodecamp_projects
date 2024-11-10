class Category:
    def __init__(self, name):
        self.name = name
        self.ledger = []

    def deposit(self, amount, description=''):
        deposit_amount = {'amount': amount, 'description': description}
        self.ledger.append(deposit_amount)

    def get_balance(self):
        return sum(item['amount'] for item in self.ledger)

    def check_funds(self, amount):
        return amount <= self.get_balance()

    def withdraw(self, amount, description=''):
        if self.check_funds(amount):
            withdraw_amount = {'amount': -amount, 'description': description}
            self.ledger.append(withdraw_amount)
            return True
        else:
            return False
      
    def transfer(self, amount, budget_category):
        if self.check_funds(amount):
            self.ledger.append({"amount": -amount, "description": f"Transfer to {budget_category.name}"})
            budget_category.ledger.append({"amount": amount, "description": f"Transfer from {self.name}"})
            return True
        return False


    def display(self):
        result = self.name.center(30, "*") + '\n'
        for item in self.ledger:
            description = item['description'][:23] 
            amount = f"{item['amount']:.2f}"[:7]
            result += f'{description.ljust(23)} {amount.rjust(7)}\n'
        total = sum(item['amount'] for item in self.ledger)
        result += f'Total: {total:.2f}'
        return result

def create_spend_chart(categories):
    result = 'Percentage spent by category\n'

    def withdrawals(category):
        total_withdrawals = 0 
        for item in category.ledger:
            if item['amount'] < 0: 
                total_withdrawals += abs(item['amount']) 
        return total_withdrawals
    total_withdrawals = sum(withdrawals(category) for category in categories)

    percentages = ((withdrawals(category) / total_withdrawals) * 100 for category in categories)
    percentages = ((percent // 10) * 10 for percent in percentages)

    for i in range(100, -1, -10):
        result += f"{str(i).rjust(3)}|"
        for percent in percentages:
            result += " o " if percent >= i else "   "
        result += "\n"

    result += "    " + "-" * (1 + 3 * len(categories)) + "\n" 

    names = [category.name for category in categories]

    max_length = max(len(name) for name in names)

    aligned_names = [name.ljust(max_length) for name in names]

    for i in range(max_length):
        line = '     ' + '  '.join(name[i] for name in padded_names) + '  '
        result += line + '\n'
    return result

