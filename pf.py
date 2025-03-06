# pf.py
from config import EMPLOYEE_CONTRIBUTION_RATE, EMPLOYER_CONTRIBUTION_RATE
from salary import Salary

class PFCalculator:
    def __init__(self, salary: Salary):
        self.salary = salary

    def calculate_employee_contribution(self):
        return self.salary.get_basic_salary() * EMPLOYEE_CONTRIBUTION_RATE

    def calculate_employer_contribution(self):
        return self.salary.get_basic_salary() * EMPLOYER_CONTRIBUTION_RATE

    def calculate_total_annual_pf(self):
        return (self.calculate_employee_contribution() + self.calculate_employer_contribution()) * 12
