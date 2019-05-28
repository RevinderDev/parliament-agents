from spade.agent import Agent
from spade.template import Template

from agents.commonBehaviours import ReceiveBehaviour
from .commonBehaviours import SendMessageBehaviour
from state import VoterDescription
from aioxmpp import JID


class VotingSystemAgent(Agent):
    async def setup(self):
        print("{} VotingSystemAgent setup".format(str(self.jid)), "\n")

    def __init__(self, jid, password, european_parliament_jid):
        super().__init__(jid, password)
        self.voters = {}
        self.europeanParliamentJID = european_parliament_jid
        self.currentStatute = None
        self.isVotingFinished = False
        self.votes = {}
        self.messageReaction = {
            "G_P_V_cs": self.process_current_statue,
            "G_P_V_ps": self.process_past_statutes,
            "I_P_V_v": self.process_submit_vote,
        }

    def receive_message_behaviour(self):
        b = ReceiveBehaviour()
        template = Template()
        template.set_metadata("performative", "inform")
        self.add_behaviour(b, template)

    def parse_message(self, msg):
        msg_code = msg.body.split("@")[0]
        self.messageReaction[msg_code](msg)

    def set_current_statute(self, statute):
        self.currentStatute = statute
        print("\tStatute: ", str(statute), "\n")

    def send_message(self, recipient, message):
        if recipient == "parliamentarians":
            for jid in self.voters:
                msg_behaviour = SendMessageBehaviour(jid, message)
                self.add_behaviour(msg_behaviour)
        else:
            msg_behaviour = SendMessageBehaviour(recipient, message)
            self.add_behaviour(msg_behaviour)

    def process_current_statue(self, msg):
        print("{} Process - current state".format(str(self.jid)))
        self.generate_current_statute(msg.sender)

    def process_past_statutes(self, msg):
        print("{} Process- previous state".format(str(self.jid)))
        self.generate_past_statutes()

    def process_submit_vote(self, msg):
        print("{} Process - actualize vote".format(str(self.jid)))
        print("\tNew vote: : {} - {}".format(str(msg.sender), str(msg.body.split("@")[1])))
        self.votes[str(msg.sender).casefold()] = int(str(msg.body).split("@")[1]) * self.voters[str(msg.sender).casefold()].strength
        if len(self.votes) == len(self.voters):
            self.generate_end_voting()
            self.isVotingFinished = True

    def generate_current_statute(self, sender):
        print("{} Generate - current state".format(str(self.jid)))
        self.send_message(recipient=sender, message="R_P_V_cs@" + str(self.currentStatute))

    def generate_past_statutes(self):
        print("{} Generate - previous state".format(str(self.jid)))
        # TODO

    def generate_set_current_statute(self):
        print("{} Generate - set current statute".format(str(self.jid)))
        self.send_message(recipient=self.europeanParliamentJID, message="I_V_E_ss@" + str(self.currentStatute))

    def generate_start_voting(self):
        print("{} Generate - start voting".format(str(self.jid)))
        self.isVotingFinished = False
        self.votes = {}
        self.generate_set_current_statute()
        self.send_message(recipient="parliamentarians", message="I_V_P_sv")

    def generate_end_voting(self):
        print("{} Generate - end voting".format(str(self.jid)))
        self.send_message(recipient="parliamentarians", message="I_V_P_ev")
        votes_summary = sum(self.votes.values())
        all_voters_strength = sum([v.strength for v in self.voters.values()])
        print("\tVotes summary: {}/{}".format(str(votes_summary), str(all_voters_strength)))
        if votes_summary >= all_voters_strength/2:
            self.generate_apply_statue()

    def generate_apply_statue(self):
        print("{} Generate - apply statute".format(str(self.jid)))
        self.send_message(recipient=self.europeanParliamentJID, message="I_V_E_as")
