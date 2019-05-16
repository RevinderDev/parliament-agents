class VoterDescription:
    def __init__(self, jid, strength, interests={}, debt=0):
        self.jid = jid
        self.strength = strength
        self.interests = interests
        self.debt = debt