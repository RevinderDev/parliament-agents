from spade.agent import Agent
from .commonBehaviours import ReceiveBehaviour
from .commonBehaviours import SendMessageBehaviour
from spade.template import Template


class EuropeanParliamentAgent(Agent):

    def __init__(self, jid, password, voting_system_id):
        super().__init__(jid, password)
        self.parliamentarian_agents_JIDs = []
        self.votingSystemId = voting_system_id
        self.current_state = []
        self.state_after_approval = []
        self.messageReaction = {
            "G_P_E_s": self.process_current_state,
            "G_P_E_as": self.process_state_after_approval,
            "I_V_E_as": self.process_apply_statue,
            "I_V_E_ss": self.process_set_current_statue
        }

    async def setup(self):
        print("EuropeanParliamentAgent {}".format(str(self.jid)))

    def receive_message_behaviour(self):
        b = ReceiveBehaviour()
        template = Template()
        template.set_metadata("performative", "inform")
        self.add_behaviour(b, template)

    def parse_message(self, msg):
        msg_code = msg.body.split("@")[0]
        self.messageReaction[msg_code](msg)

    def process_current_state(self, msg):
        print("{} Process - current state".format(str(self.jid)))

    def process_state_after_approval(self, msg):
        print("{} Process - state after aproval".format(str(self.jid)))

    def process_apply_statue(self, msg):
        print("{} Process - apply statue".format(str(self.jid)))

    def process_set_current_statue(self, msg):
        print("{} Process - set current statue".format(str(self.jid)))

    def generate_current_state(self):
        print("{} Generate - current state".format(str(self.jid)))

    def generate_state_after_approval(self):
        print("{} Generate - state after aproval".format(str(self.jid)))
