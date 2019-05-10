class Statute:
    id_count = 0

    def __init__(self, interests):
        self.id = self.__class__.id_count
        self.__class__.id_count += 1
        self.interests = interests

    def __str__(self):
        return "[STATUTE: id = " + str(self.id) + ", interests = " + str(self.interests) + "]"

    def __repr__(self):
        return "[STATUTE: id = " + str(self.id) + "]"
