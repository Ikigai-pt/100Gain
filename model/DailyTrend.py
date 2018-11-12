from datetime import date
class DailyTrend:
    price = 0.0
    action = 'Monitoring'
    percentageChangeSinceTracking = 0.0
    percentageChange = 0.0
    category = None
    direction = None
    reportedDate= date.today()

    def __init__(self, price, action, pChangeSinceTracking, pChange, category, direction ):
        self.price = price
        self.action = action
        self.percentageChangeSinceTracking = pChangeSinceTracking
        self.percentageChange = pChange
        self.category = category
        self.direction = direction

    def setPercentageChangeSinceTracking(self, pChange):
        self.percentageChangeSinceTracking = pChange

