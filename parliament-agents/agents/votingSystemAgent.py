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
        self.code_messages = {
            "R_P_V_cs": self.generate_current_statue,
            "R_P_V_ps": self.generate_previous_state,
            "I_V_P_v": self.generate_future_union_state,
        }

    def receive_message_behaviour(self):
        b = ReceiveBehaviour()
        template = Template()
        template.set_metadata("performative", "inform") #TODO: Problem z odbieraniem czy co?
        self.add_behaviour(b, template)

    def parse_message(self, msg):
        msg_code = msg.body.split("@")[0]
        response = self.code_messages[msg_code]()
        # msg_behaviour = SendMessageBehaviour(msg._sender, msg_code.join(response))
        # self.add_behaviour(msg_behaviour)

    def send_message(self, recipient, message_code):
        if recipient == "parliamentarians":
            for jid in self.parliamentarian_agents_JIDs:
                msg_behaviour = SendMessageBehaviour(jid, message_code)
                self.add_behaviour(msg_behaviour)

    def generate_current_statue(self):
        print("{} Answer - current state".format(str(self.jid)))
        return "CurrentState"

    def generate_previous_state(self):
        print("{} Answer - previous state".format(str(self.jid)))
        return "PreviousState"

    def generate_future_union_state(self):
        print("{} Answer - calculate future union state".format(str(self.jid)))
        return "TestFutureUnion"

    def start_vote(self):
        print("{} start voting".format(str(self.jid)))
        self.send_message(recipient="parliamentarians", message_code="I_V_P_sv")

    def actualize_vote(self):
        print("{} actualize vote".format(str(self.jid)))

    def end_vote(self):
        print("{} end vote".format(str(self.jid)))

    def apply_current_statue(self):
        print("{} apply statue".format(str(self.jid)))
