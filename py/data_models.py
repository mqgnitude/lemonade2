from dataclasses import dataclass, field
from typing import List, Dict

@dataclass
class Product:
    base_demand: int = 100
    reference_price: float = 20.0
    elasticity: float = 1.5
    cost_per_unit: float = 8.0

@dataclass
class Difficulty:
    name: str
    starting_cash: float
    volatility: float
    supplier_reliability: float
    tax_rate: float

@dataclass
class GameState:
    difficulty: str = "Medium"
    month: int = 1
    year: int = 1
    cash: float = 1000.0
    inventory: int = 50
    price: float = 25.0
    marketing_spend: float = 50.0
    loan_balance: float = 0.0
    employees: int = 1
    employee_wage: float = 200.0
    total_revenue: float = 0.0
    total_profit: float = 0.0
    last_turn_log: List[str] = field(default_factory=list)
    history: List[Dict] = field(default_factory=list)

    def to_dict(self):
        return self.__dict__

    @staticmethod
    def from_dict(data):
        state = GameState()
        for key, value in data.items():
            if hasattr(state, key):
                setattr(state, key, value)
        return state