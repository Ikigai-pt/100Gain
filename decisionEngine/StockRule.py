from decisionEngine.DecisionTables import load_xls, process_dt

DEFAULT_RULE = {"day1": "'N'", "day2": "'N'", "day3": "'N'", "Action": '"None"'}
RULE_BOOK = load_xls('./decisionEngine/Rule.xls')

def applyRule(recentTrends):
    trends = [r for r in recentTrends]
    rule = DEFAULT_RULE
    for stock in trends:
        if stock.changePercent > 0.0 :
            rule["day"+str(stock.dayNumber)] = "'H'"
        else:
            rule["day"+str(stock.dayNumber)] = "'L'"
    process_dt(rule, RULE_BOOK)
    print(rule)
    return rule["Action"].replace('"', '')
