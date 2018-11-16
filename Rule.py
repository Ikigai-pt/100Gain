from RuleSet import rules
from business_rules import run_all
from business_rules.variables import *
from business_rules.actions import *
from DecisionTables import *

import datetime
FIELD_NUMERIC = 'numeric'
FIELD_SELECT = 'select'

class ProductVariables(BaseVariables):

    def __init__(self, product):
        self.product = product

    @numeric_rule_variable
    def current_inventory(self):
        return self.product.current_inventory

class ProductActions(BaseActions):

    def __init__(self, product):
        self.product = product

    @rule_action(params={"sale_percentage": FIELD_NUMERIC})
    def put_on_sale(self, sale_percentage):
        self.product.price = (1.0 - sale_percentage) * self.product.price

    # @rule_action(params=[{'fieldType': FIELD_SELECT,
    #                       'name': 'stock_state',
    #                       'label': 'Stock state',
    #                       'options': [
    #                         {'label': 'Available', 'name': 'available'},
    #                         {'label': 'Last items', 'name': 'last_items'},
    #                         {'label': 'Out of stock', 'name': 'out_of_stock'}
    #                     ]}])
    # def change_stock_state(self, stock_state):
    #     self.product.stock_state = stock_state
    #     self.product.save()

class Product:
    def __init__(self, inventory, price):
        self.current_inventory = inventory
        self.price = price

product = Product(20,200)

run_all(rule_list=rules,
        defined_variables=ProductVariables(product),
        defined_actions=ProductActions(product),
        stop_on_first_trigger=True
    )

tbl = load_xls('Rule.xls')
test_fact = { "Day1" : "'H'", "Day2" : "'L'", "Day3": "'L'"}
process_dt(test_fact, tbl)
print(test_fact)
