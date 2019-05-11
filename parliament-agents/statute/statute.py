from interest.interest import Interest
import json


class Statute:
    id_count = 0

    def __init__(self, interests, id_set=-1):
        if id_set == -1:
            self.id = self.__class__.id_count
        else:
            self.id = id_set
        self.__class__.id_count += 1
        self.interests = interests

    def __str__(self):
        return "[STATUTE: id = " + str(self.id) + ", interests = [" + " ".join([str(i) for i in self.interests]) + "]]"

    def __repr__(self):
        return "[STATUTE: id = " + str(self.id) + "]"

    @staticmethod
    def str_to_statute(string):
        id_set = int(string.split("id = ")[1].split(",")[0])
        interests = []
        for s in string.split("interests = ")[1].split("INTEREST: ")[1:]:
            interests.append(Interest.str_to_interest(s.replace(']', '').replace('[', '')))
        return Statute(interests, id_set)
