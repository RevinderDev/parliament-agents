class InterestArea:
    def __init__(self, name, attitude_left, attitude_right):
        self.name = name
        self.attitudeLeft = attitude_left
        self.attitudeRight = attitude_right

    def __str__(self):
        return "[INTEREST_AREA: name = " + self.name + ", left = " + str(self.attitudeLeft) + ", right = " \
               + str(self.attitudeRight) + "]"

    def __repr__(self):
        return "[INTEREST_AREA: name = " + self.name + "]"

    def __hash__(self):
        return hash((self.name, self.attitudeLeft, self.attitudeRight))

    def __eq__(self, other):
        return (self.name, self.attitudeLeft, self.attitudeRight) == \
               (other.name, other.attitudeLeft, other.attitudeRight)

