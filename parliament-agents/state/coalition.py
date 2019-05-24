class Coalition:
    def __init__(self, vote, debt, sender, reciver, responded):
        self.vote = vote
        self.debt = debt
        self.sender = sender
        self.reciver = reciver
        self.responded = responded
        self.accept = None