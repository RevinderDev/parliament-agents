from spade.agent import Agent
from spade.template import Template

from agents.commonBehaviours import ReceiveBehaviour
from .commonBehaviours import SendMessageBehaviour


class VotingSystemAgent(Agent):
    async def setup(self):
        print("Voting system agent starts")
        self.presence.set_available()

    def __init__(self, jid, password):
        super().__init__(jid, password)
        self.parliamentarian_agents_JIDs = []
        self.messageReaction = {
            "G_P_V_cs": self.process_current_statue,
            "G_P_V_ps": self.process_past_statutes,
            "I_P_V_v": self.process_submit_vote,
        }

    def receive_message_behaviour(self):
        b = ReceiveBehaviour()
        template = Template()
        template.set_metadata("performative", "inform") #TODO: Problem z odbieraniem czy co?
        self.add_behaviour(b, template)

    def parse_message(self, msg):
        msg_code = msg.body.split("@")[0]
        self.messageReaction[msg_code](msg)
        # msg_behaviour = SendMessageBehaviour(msg._sender, msg_code.join(response))
        # self.add_behaviour(msg_behaviour)

    def send_message(self, recipient, message_code):
        if recipient == "parliamentarians":
            for jid in self.parliamentarian_agents_JIDs:
                msg_behaviour = SendMessageBehaviour(jid, message_code)
                self.add_behaviour(msg_behaviour)

    def process_current_statue(self, msg):
        print("{} Process - current state".format(str(self.jid)))
        self.generate_current_statute()

    def process_past_statutes(self, msg):
        print("{} Process- previous state".format(str(self.jid)))
        self.generate_past_statutes()

    def process_submit_vote(self, msg):
        print("Process {} actualize vote".format(str(self.jid)))

    def generate_current_statute(self, msg):
        print("{} Generate - current state".format(str(self.jid)))

    def generate_past_statutes(self):
        print("{} Generate - previous state".format(str(self.jid)))

    def generate_set_current_statute(self):
        print("{} Generate - set current statute".format(str(self.jid)))

    def generate_start_voting(self):
        print("Generate {} start voting".format(str(self.jid)))
        self.send_message(recipient="parliamentarians", message_code="I_V_P_sv")

    def generate_end_voting(self):
        print("Generate {} end vote".format(str(self.jid)))

    def generate_apply_statue(self):
        print("Generate {} apply statue".format(str(self.jid)))
