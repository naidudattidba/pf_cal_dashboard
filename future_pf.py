# future_pf.py
from config import INTEREST_RATE
from pf import PFCalculator
import pandas as pd

class FuturePF:
    def __init__(self, pf_calculator: PFCalculator, current_pf_balance: float, years: int, annual_hike: float):
        self.pf_calculator = pf_calculator
        self.current_pf_balance = current_pf_balance
        self.years = years
        self.annual_hike = annual_hike  # Percentage increase in salary each year

    def calculate_future_pf(self):
        balance = self.current_pf_balance
        salary = self.pf_calculator.salary.get_basic_salary()

        data = []
        for year in range(1, self.years + 1):
            annual_pf = self.pf_calculator.calculate_total_annual_pf()
            balance += annual_pf  # Add yearly PF contributions
            balance += balance * INTEREST_RATE  # Apply yearly interest
            
            # Store yearly data
            data.append({"Year": year, "Salary": salary, "Annual PF": annual_pf, "Total PF Balance": balance})

            # Increase salary
            salary += salary * self.annual_hike
            self.pf_calculator.salary.basic_salary = salary

        return pd.DataFrame(data)  # Return DataFrame for visualization
