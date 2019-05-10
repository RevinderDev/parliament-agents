class Interest:
    def __init__(self, interest_area, attitude, strength):
        self.interestArea = interest_area
        self.attitude = attitude
        self.strength = strength

    def __str__(self):
        return "[INTEREST: interest_area = " + self.interestArea.name + ", attitude = " + self.attitude \
               + ", strength = " + self.strength + "]"

    def __repr__(self):
        return "[INTEREST: interest_area = " + self.interestArea.name + "]"
