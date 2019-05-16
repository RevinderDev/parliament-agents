from interest.interest import Interest
from interest.interestArea import InterestArea
import json


class UnionState:
    id_count = 0

    def __init__(self, state):
        self.state = state

    def __str__(self):
        return "[UNIONSTATE: state = [" + " ".join(["[ INTEREST_AREA_VALUE: interest_area = " + k.name + ", value = " + str(i) + "]" for k, i in self.state.items()]) + "]]"

    def __repr__(self):
        return "[UNIONSTATE: ]"

    @staticmethod
    def str_to_state(string):
        state = {}
        for s in string.split("state = ")[1].split("INTEREST_AREA_VALUE: ")[1:]:
            split = s.replace(']', '').replace('[', '').split("= ")
            state[InterestArea(split[1].split(",")[0], "", "")] = float(split[2])
        return UnionState(state)
