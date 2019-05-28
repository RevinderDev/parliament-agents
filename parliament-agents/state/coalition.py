class Coalition:
    def __init__(self, vote, debt, sender, receiver, responded):
        self.vote = vote
        self.debt = debt
        self.sender = sender
        self.receiver = receiver
        self.responded = responded
        self.accept = None