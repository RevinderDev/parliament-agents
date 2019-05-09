class Statute:
    id_count = 0

    def __init__(self, interests):
        self.id = self.__class__.id_count
        self.__class__.id_count += 1
        self.interests = interests
