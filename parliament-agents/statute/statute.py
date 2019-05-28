from interest.interest import Interest
from interest.interestArea import InterestArea
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
        self.reference = None
        self.title = None
        self.subject = None

    def __str__(self):
        return "[STATUTE: id = " + str(self.id) + ", interests = [" + " ".join(
            [str(i) for k, i in self.interests.items()]) + "]]"

    def __repr__(self):
        return "[STATUTE: id = " + str(self.id) + "]"

    def with_title(self, title):
        self.title = title
        return self

    def with_reference(self, reference):
        self.reference = reference
        return self

    def with_subject(self, subject):
        self.subject = subject
        return self

    @staticmethod
    def str_to_statute(string):
        id_set = int(string.split("id = ")[1].split(",")[0])
        interests = {}
        for s in string.split("interests = ")[1].split("INTEREST: ")[1:]:
            interest = Interest.str_to_interest(s.replace(']', '').replace('[', ''))
            interests[InterestArea(interest.interestAreaName, "", "")] = interest
        return Statute(interests, id_set)

    @staticmethod
    def json_to_statute(json_dict):
        interests = {}
        for entry in json_dict['interests']:
            interest = Interest(entry['interestArea'], entry['attitude'], entry['strength'])
            # TODO: missing attitudes (left/right) in data set
            interests[InterestArea(interest.interestAreaName, attitude_left="", attitude_right="")] = interest

        return Statute(interests) \
            .with_reference(json_dict['reference']) \
            .with_subject(json_dict['subject']) \
            .with_title(json_dict['title'])
