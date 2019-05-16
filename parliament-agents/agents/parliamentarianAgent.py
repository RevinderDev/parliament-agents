from spade.agent import Agent
from .commonBehaviours import ReceiveBehaviour
from .commonBehaviours import SendMessageBehaviour
from spade.template import Template
from random import randint
from math import sqrt


class ParliamentarianAgent(Agent):
    id_count = 0

    def __init__(self, jid, password, voting_system_id, interests):
        super().__init__(jid, password)
        self.votingSystemId = voting_system_id
        self.interests = interests
        self.id = self.__class__.id_count
        self.__class__.id_count += 1
        self.messageReaction = {
            "G_P_P_i": self.process_information_about_interests,
            "G_P_P_a": self.process_information_about_attitude,
            "R_P_P_i": self.process_response_information_about_interests,
            "R_P_P_a": self.process_response_information_about_attitude,
            "S_pc": self.process_coalition_proposition,
            "S_ac": self.process_coalition_acceptation,
            "S_rc": self.process_coalition_refusal,
            "R_P_E_s": self.process_current_state,
            "R_P_E_as": self.process_current_state_after_approval,
            "R_P_V_cs": self.process_current_statute,
            "R_P_V_ps": self.process_past_statutes,
            "I_V_P_sv": self.process_start_voting,
            "I_V_P_ev": self.process_end_voting
        }

    async def setup(self):
        print("{} ParliamentarianAgent setup".format(str(self.jid)))
        print("\tInterests: ", self.interests, "\n")

    def receive_message_behaviour(self):
        b = ReceiveBehaviour()
        template = Template()
        template.set_metadata("performative", "inform")
        self.add_behaviour(b, template)

    def parse_message(self, msg):
        msg_code = msg.body.split("@")[0]
        self.messageReaction[msg_code](msg)

    def process_information_about_interests(self, msg):
        print("{} Process - interests".format(str(self.jid)))
        # TODO analyze information received

    def process_information_about_attitude(self, msg):
        print("{} Process - attitude".format(str(self.jid)))
        # TODO analyze information received

    def process_response_information_about_interests(self, msg):
        print("{} Process - interests".format(str(self.jid)))

    def process_response_information_about_attitude(self, msg):
        print("{} Process - attitude".format(str(self.jid)))

    def process_coalition_proposition(self, msg):
        print("{} Process - coalition proposition".format(str(self.jid)))
        # TODO analyze proposition and send response

    def process_coalition_acceptation(self, msg):
        print("{} Process - coalition acceptation".format(str(self.jid)))
        # TODO analyze information received

    def process_coalition_refusal(self, msg):
        print("{} Process - coalition refusal".format(str(self.jid)))
        # TODO analyze information received

    def process_current_state(self, msg):
        print("{} Process - current state".format(str(self.jid)))
        # TODO analyze information received

    def process_current_state_after_approval(self, msg):
        print("{} Process - state after approval".format(str(self.jid)))
        # TODO analyze information received

    def process_current_statute(self, msg):
        print("{} Process - current statute".format(str(self.jid)))
        # TODO analyze information received

    def process_past_statutes(self, msg):
        print("{} Process - past statutes".format(str(self.jid)))

    def process_start_voting(self, msg):
        print("{} Process - start voting".format(str(self.jid)))
        # TODO generate some actions to create coalition
        self.generate_submit_vote()

    def process_end_voting(self, msg):
        print("{} Process - end voting".format(str(self.jid)))
        # TODO ask about results and actualize information

    def generate_information_about_interests(self):
        print("{} Generate - interests".format(str(self.jid)))
        # TODO send

    def generate_information_about_attitude(self):
        print("{} Generate - attitude".format(str(self.jid)))
        # TODO send

    def generate_coalition_proposition(self):
        print("{} Generate Coalition - propose".format(str(self.jid)))
        # TODO send

    def generate_coalition_acceptation(self):
        print("{} Generate Coalition - accept".format(str(self.jid)))
        # TODO send

    def generate_coalition_refusal(self):
        print("{} Generate Coalition - reject".format(str(self.jid)))
        # TODO send

    def generate_current_state(self):
        print("{} Generate - current state".format(str(self.jid)))
        # TODO send

    def generate_current_state_after_approval(self):
        print("{} Generate - state after approval".format(str(self.jid)))
        # TODO send

    def generate_current_statute(self):
        print("{} Generate - current statute".format(str(self.jid)))
        # TODO send

    def generate_past_statutes(self):
        print("{} Generate - past statutes".format(str(self.jid)))
        # TODO send

    def generate_submit_vote(self):
        print("{} Generate - submit vote".format(str(self.jid)))
        vote = randint(0, 1)  # TODO Decide how to vote (now only random)
        print("\tVote: " + str(vote))
        b = SendMessageBehaviour(self.votingSystemId, "I_P_V_v@" + str(vote))
        self.add_behaviour(b)

    def calculate_distance_to_union_state(self, dict_of_interest, state):
        d = 0
        for area, i in dict_of_interest.items():
            v = state.state[area]
            d += (v - i.attitude) * (v - i.attitude) * i.strength
        return sqrt(d)
