class Interest:
    def __init__(self, interest_area_name, attitude, strength):
        self.interestAreaName = interest_area_name
        self.attitude = attitude
        self.strength = strength

    def __str__(self):
        return "[INTEREST: interest_area = " + self.interestAreaName + ", attitude = " + str(self.attitude) \
               + ", strength = " + str(self.strength) + "]"

    def __repr__(self):
        return "[INTEREST: interest_area = " + self.interestAreaName + "]"

    @staticmethod
    def str_to_interest(string):
        split = string.split("= ")
        return Interest(split[1].split(",")[0], float(split[2].split(",")[0]), float(split[3]))
