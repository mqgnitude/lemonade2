import math
import random
from py.data_models import GameState, Product, Difficulty

DIFFICULTIES = {
    "Easy": Difficulty("Easy", 2000.0, 0.05, 0.95, 0.15),
    "Medium": Difficulty("Medium", 1000.0, 0.10, 0.85, 0.20),
    "Hard": Difficulty("Hard", 500.0, 0.20, 0.70, 0.25)
}

class Engine:
    def __init__(self, difficulty_name="Medium"):
        self.diff_config = DIFFICULTIES.get(difficulty_name, DIFFICULTIES["Medium"])
        self.state = GameState(difficulty=difficulty_name, cash=self.diff_config.starting_cash)
        self.product = Product()

    def calculate_demand(self):
        base = self.product.base_demand
        price_ratio = self.product.reference_price / max(0.1, self.state.price)
        price_factor = price_ratio ** self.product.elasticity
        marketing_scale = 200 
        marketing_factor = 1 + (self.state.marketing_spend / (self.state.marketing_spend + marketing_scale))
        seasonal_factor = 1 + 0.1 * math.sin(2 * math.pi * self.state.month / 12)
        volatility = self.diff_config.volatility
        noise = random.uniform(1 - volatility, 1 + volatility)
        raw_demand = base * price_factor * marketing_factor * seasonal_factor * noise
        return int(max(0, raw_demand))

    def process_turn(self):
        logs = []
        potential_sales = self.calculate_demand()
        units_sold = min(potential_sales, self.state.inventory)
        lost_sales = potential_sales - units_sold
        revenue = units_sold * self.state.price
        variable_costs = units_sold * self.product.cost_per_unit 
        payroll = self.state.employees * self.state.employee_wage
        interest = self.state.loan_balance * (0.05 / 12)
        fixed_costs = 100.0
        total_expenses = fixed_costs + payroll + interest + self.state.marketing_spend
        operating_profit = revenue - variable_costs - total_expenses
        tax = 0.0
        if operating_profit > 0:
            tax = operating_profit * self.diff_config.tax_rate
        net_profit = operating_profit - tax
        cash_outflows = total_expenses + tax
        self.state.cash += revenue
        self.state.cash -= cash_outflows
        self.state.inventory -= units_sold
        self.state.total_revenue += revenue
        self.state.total_profit += net_profit
        
        logs.append(f"Sold {units_sold} units (Lost {lost_sales} due to stock).")
        logs.append(f"Revenue: ${revenue:.2f}. Net Profit: ${net_profit:.2f}.")
        logs.append(f"Cash changed by ${revenue - cash_outflows:.2f}.")
        if self.state.cash < 0:
            logs.append("WARNING: You are in debt! Bankruptcy looms.")
        
        self.state.history.append({"month": self.state.month, "cash": self.state.cash, "profit": net_profit})
        self.state.month += 1
        if self.state.month > 12:
            self.state.month = 1
            self.state.year += 1
        self.state.last_turn_log = logs
        return logs

    def buy_inventory(self, amount):
        cost = amount * self.product.cost_per_unit
        if cost > self.state.cash:
            return False, "Not enough cash!"
        if random.random() > self.diff_config.supplier_reliability:
            amount = int(amount * 0.5)
            self.state.cash -= cost 
            self.state.inventory += amount
            return True, f"Supplier issues! You paid full price but only received {amount} units."
        self.state.cash -= cost
        self.state.inventory += amount
        return True, f"Bought {amount} units for ${cost:.2f}."

    def hire_employee(self):
        self.state.employees += 1
        return "Hired a new worker. Productivity up, payroll up."

    def fire_employee(self):
        if self.state.employees > 0:
            self.state.employees -= 1
            return "Fired a worker. Morale is low."
        return "No one left to fire!"
    
    def take_loan(self, amount):
        self.state.cash += amount
        self.state.loan_balance += amount
        return f"Took loan of ${amount}."

    def repay_loan(self, amount):
        if amount > self.state.cash:
            return False, "Not enough cash."
        if amount > self.state.loan_balance:
            amount = self.state.loan_balance
        self.state.cash -= amount
        self.state.loan_balance -= amount
        return True, f"Repaid ${amount} of loan." 