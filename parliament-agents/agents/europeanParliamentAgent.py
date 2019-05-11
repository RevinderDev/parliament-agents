from spade.agent import Agent
from .commonBehaviours import ReceiveBehaviour
from .commonBehaviours import SendMessageBehaviour
from spade.template import Template
from statute import Statute


class EuropeanParliamentAgent(Agent):

    def __init__(self, jid, password, voting_system_id, state):
        super().__init__(jid, password)
        self.parliamentarianAgentsJIDs = []
        self.votingSystemId = voting_system_id
        self.currentState = state
        self.stateAfterApproval = {}
        self.messageReaction = {
            "G_P_E_s": self.process_current_state,
            "G_P_E_as": self.process_state_after_approval,
            "I_V_E_as": self.process_apply_statue,
            "I_V_E_ss": self.process_set_current_statue
        }

    async def setup(self):
        print("{} EuropeanParliamentAgent setup".format(str(self.jid)))
        print("\tState: ", str(self.currentState), "\n")

    def receive_message_behaviour(self):
        b = ReceiveBehaviour()
        template = Template()
        template.set_metadata("performative", "inform")
        self.add_behaviour(b, template)

    def parse_message(self, msg):
        msg_code = msg.body.split("@")[0]
        self.messageReaction[msg_code](msg)

    def set_current_state(self, state):
        self.currentState = state
        print("\tNew state: ", str(state), "\n")

    def calculate_state_after_approval(self, statute):
        # TODO calculate
        self.stateAfterApproval = self.currentState
        print("\tState after approval: " + str(self.stateAfterApproval))

    def process_current_state(self, msg):
        print("{} Process - current state".format(str(self.jid)))
        self.generate_current_state(msg.sender)

    def process_state_after_approval(self, msg):
        print("{} Process - state after approval".format(str(self.jid)))
        self.generate_state_after_approval(msg.sender)

    def process_apply_statue(self, msg):
        print("{} Process - apply statute".format(str(self.jid)))
        self.currentState = self.stateAfterApproval

    def process_set_current_statue(self, msg):
        print("{} Process - set current statute".format(str(self.jid)))
        statute = Statute.str_to_statute(str(msg.body).split("@")[1])
        self.calculate_state_after_approval(statute)

    def generate_current_state(self, recipient):
        print("{} Generate - current state".format(str(self.jid)))
        b = SendMessageBehaviour(recipient, "R_P_E_s@" + str(self.currentState))
        self.add_behaviour(b)

    def generate_state_after_approval(self, recipient):
        print("{} Generate - state after approval".format(str(self.jid)))
        b = SendMessageBehaviour(recipient, "R_P_E_as@" + str(self.stateAfterApproval))
        self.add_behaviour(b)
