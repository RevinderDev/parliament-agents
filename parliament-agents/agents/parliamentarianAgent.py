from spade.agent import Agent
from .commonBehaviours import ReceiveBehaviour
from .commonBehaviours import SendMessageBehaviour
from spade.template import Template
from math import sqrt
from state import UnionState, VoterDescription, Coalition
from interest import Interest, InterestArea
from .parliamentarianBehaviours import VoteAfterTime


class ParliamentarianAgent(Agent):
    id_count = 0

    def __init__(self, jid, password, voting_system_id, european_parliament_id, interests, strength, name):
        super().__init__(jid, password)
        self.votingSystemId = voting_system_id
        self.europeanParliamentId = european_parliament_id
        self.interests = interests
        self.strength = strength
        self.party_name = name
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
        self.voters = {}
        # Agent must be interested in voting more then that to make propositions
        self.minimal_interest = 1
        self.currentUnionState = None
        self.unionStateAfterApproval = None
        self.interestInApprove = None
        self.all_data = False
        self.other_coalitions = {}
        self.my_coalitions = {}
        self.vote = None
        self.voters_id_to_address = None
        self.voters_address_to_id = None

    async def setup(self):
        print("{} ParliamentarianAgent setup".format(str(self.jid)))
        print("\tInterests: ", self.interests, "\n")

    def receive_message_behaviour(self):
        b = ReceiveBehaviour()
        template = Template()
        template.set_metadata("performative", "inform")
        self.add_behaviour(b, template)

    def vote_after_time_behaviour(self):
        b = VoteAfterTime()
        template = Template()
        template.set_metadata("performative", "inform")
        self.add_behaviour(b, template)

    def parse_message(self, msg):
        msg_code = msg.body.split("@")[0]
        self.messageReaction[msg_code](msg)

    def process_information_about_interests(self, msg):
        print("{} Process - interests".format(str(self.jid)))
        interests_of = int(msg.body.split("@")[1])
        response = "R_P_P_i@" + str(interests_of) + "@"
        if interests_of == self.id:
            response += " ".join([str(i) for k, i in self.interests.items()])
        else:
            response += " ".join([str(i) for k, i in self.voters[interests_of].interests.items()])
        b = SendMessageBehaviour(msg.sender, response)
        self.add_behaviour(b)

    def process_information_about_attitude(self, msg):
        print("{} Process - attitude".format(str(self.jid)))
        # TODO analyze information received

    def process_response_information_about_interests(self, msg):
        print("{} Process - interests".format(str(self.jid)))
        split = msg.body.split("@")
        interests_of = int(split[1])
        interests = {}
        for s in split[2].split("INTEREST: ")[1:]:
            interest = Interest.str_to_interest(s.replace(']', '').replace('[', ''))
            interests[InterestArea(interest.interestAreaName, "", "")] = interest
        self.voters[interests_of].interests = interests

    def process_response_information_about_attitude(self, msg):
        print("{} Process - attitude".format(str(self.jid)))

    def process_coalition_proposition(self, msg):
        print("{} Process - coalition proposition".format(str(self.jid)))
        other_id = self.voters_address_to_id[str(msg.sender).casefold()]
        args = msg.body.split("@")
        vote = args[1]
        debt = args[2]
        self.other_coalitions[other_id] = Coalition(int(vote), float(debt), other_id, self.id, False)

    def process_coalition_acceptation(self, msg):
        print("{} Process - coalition acceptation".format(str(self.jid)))
        other_id = self.voters_address_to_id[str(msg.sender).casefold()]
        self.my_coalitions[other_id].responded = True
        self.my_coalitions[other_id].accept = True
        self.voters[other_id].debt -= self.my_coalitions[other_id].debt

    def process_coalition_refusal(self, msg):
        print("{} Process - coalition refusal".format(str(self.jid)))
        other_id = self.voters_address_to_id[str(msg.sender).casefold()]
        self.my_coalitions[other_id].responded = True
        self.my_coalitions[other_id].accept = False

    def process_current_state(self, msg):
        print("{} Process - current state".format(str(self.jid)))
        self.currentUnionState = UnionState.str_to_state(msg.body.split("@")[1])

    def process_current_state_after_approval(self, msg):
        print("{} Process - state after approval".format(str(self.jid)))
        self.unionStateAfterApproval = UnionState.str_to_state(msg.body.split("@")[1])

    def process_current_statute(self, msg):
        print("{} Process - current statute".format(str(self.jid)))
        # TODO analyze information received

    def process_past_statutes(self, msg):
        print("{} Process - past statutes".format(str(self.jid)))

    def process_start_voting(self, msg):
        print("{} Process - start voting".format(str(self.jid)))
        self.currentUnionState = None
        self.unionStateAfterApproval = None
        self.interestInApprove = None
        self.all_data = False
        self.other_coalitions = {}
        self.my_coalitions = {}
        self.vote = None
        self.generate_get_current_state()
        self.generate_get_state_after_approval()
        for id, v in self.voters.items():
            if len(v.interests) == 0 and id != self.id:
                self.generate_information_about_interests(self.voters_id_to_address[id], id)
        self.vote_after_time_behaviour()

    def generate_get_current_state(self):
        print("{} Generate - get current Union state".format(str(self.jid)))
        b = SendMessageBehaviour(self.europeanParliamentId, "G_P_E_s@")
        self.add_behaviour(b)

    def generate_get_state_after_approval(self):
        print("{} Generate - get current Union state after approval".format(str(self.jid)))
        b = SendMessageBehaviour(self.europeanParliamentId, "G_P_E_as@")
        self.add_behaviour(b)

    def process_end_voting(self, msg):
        print("{} Process - end voting".format(str(self.jid)))
        # TODO ask about results and actualize information

    def generate_information_about_interests(self, asked, interests_of):
        print("{} Generate - interests of {}, asked {}".format(str(self.jid), interests_of, asked))
        b = SendMessageBehaviour(asked, "G_P_P_i@" + str(interests_of))
        self.add_behaviour(b)

    def generate_information_about_attitude(self):
        print("{} Generate - attitude".format(str(self.jid)))
        # TODO send

    def generate_coalition_proposition(self, coalition):
        print("{} Generate Coalition - propose".format(str(self.jid)))
        self.my_coalitions[coalition.receiver] = coalition
        b = SendMessageBehaviour(self.voters_id_to_address[coalition.receiver], "S_pc@" + str(coalition.vote) + "@" + str(coalition.debt))
        self.add_behaviour(b)

    def generate_coalition_acceptation(self, coalition):
        print("{} Generate Coalition - accept".format(str(self.jid)))
        self.other_coalitions[coalition.sender].responded = True
        self.other_coalitions[coalition.sender].accept = True
        self.voters[coalition.sender].debt += coalition.debt
        b = SendMessageBehaviour(self.voters_id_to_address[coalition.sender], "S_ac@")
        self.add_behaviour(b)

    def generate_coalition_refusal(self, coalition):
        print("{} Generate Coalition - reject".format(str(self.jid)))
        self.other_coalitions[coalition.sender].responded = True
        self.other_coalitions[coalition.sender].accept = False
        b = SendMessageBehaviour(self.voters_id_to_address[coalition.sender], "S_rc@")
        self.add_behaviour(b)

    def generate_current_statute(self):
        print("{} Generate - current statute".format(str(self.jid)))
        # TODO send

    def generate_past_statutes(self):
        print("{} Generate - past statutes".format(str(self.jid)))
        # TODO send

    def generate_submit_vote(self):
        print("{} Generate - submit vote".format(str(self.jid)))
        print("\tVote: " + str(self.vote))
        b = SendMessageBehaviour(self.votingSystemId, "I_P_V_v@" + str(self.vote))
        self.add_behaviour(b)

    def has_all_data(self):
        if self.all_data:
            return True
        if self.currentUnionState is None:
            print("{} Wait for union state".format(str(self.jid)))
            return False
        if self.unionStateAfterApproval is None:
            print("{} Wait for union state after approval".format(str(self.jid)))
            return False
        if self.interestInApprove is None:
            current_dist = self.calculate_distance_to_union_state(self.interests, self.currentUnionState)
            after_approval_dist = self.calculate_distance_to_union_state(self.interests, self.unionStateAfterApproval)
            print("{} currentDist {}; afterApprovalDist {}".format(str(self.jid), current_dist, after_approval_dist))
            self.interestInApprove = {self.id: current_dist - after_approval_dist}
            print("{} interest in approve {}".format(str(self.jid), self.interestInApprove[self.id]))
        for id, v in self.voters.items():
            if len(v.interests) == 0 and id != self.id:
                print("{} Wait for interest of {}".format(str(self.jid), id))
                return False
        for id, v in self.voters.items():
            if id == self.id:
                continue
            current_dist = self.calculate_distance_to_union_state(v.interests, self.currentUnionState)
            after_approval_dist = self.calculate_distance_to_union_state(v.interests, self.unionStateAfterApproval)
            self.interestInApprove[id] = current_dist - after_approval_dist
        self.all_data = True
        print("{} all data collected".format(str(self.jid)))
        return True

    def post_vote(self):
        print("{} already decided {}".format(str(self.jid), self.vote))
        for c in self.other_coalitions.values():
            if not c.responded:
                if c.vote != self.vote:
                    self.generate_coalition_refusal(c)
                else:
                    self.generate_coalition_acceptation(c)

    def calculate_possible_votes(self, my_vote):
        # find out who may vote as we and how many voters is there
        votes_on_our_side = self.strength
        all_voters_strength = 0
        # we know how these agents are voting
        known_vote = set()
        known_vote.add(self.id)
        for id, interest in self.interestInApprove.items():
            all_voters_strength += self.voters[id].strength
            # add everyone who has above minimal interest in this statute
            if abs(interest) >= self.minimal_interest and not id in known_vote:
                if interest * my_vote[0] > 0:
                    known_vote.add(id)
                    votes_on_our_side += self.voters[id].strength
        for id, c in self.my_coalitions.items():
            # add everyone who accept our coalition
            if c.responded and c.accept and not id in known_vote:
                known_vote.add(id)
                votes_on_our_side += self.voters[id].strength
        for id, c in self.other_coalitions.items():
            # we may immediatly accept coalitions that have same vote as us
            if c.vote == my_vote[1] and not id in known_vote:
                known_vote.add(id)
                votes_on_our_side += self.voters[id].strength
        print("{} think: votes on our side {}; all voters {}".format(str(self.jid), votes_on_our_side, all_voters_strength))
        return votes_on_our_side, all_voters_strength

    def calculate_possible_votes_to_convince(self, my_vote, list_to_convince):
        possible_votes = self.strength * my_vote[0]
        for id, dist in list_to_convince:
            if abs(self.interestInApprove[self.id]) >= self.minimal_interest:
                if dist > 0:
                    possible_votes += self.voters[id].strength
                else:
                    possible_votes -= self.voters[id].strength
        return possible_votes

    def choose_better_propositions(self, need_to_made_choice=False):
        print("{} not interested in voting".format(str(self.jid)))
        # favour our standing
        debt = self.interestInApprove[self.id]
        if len(self.other_coalitions) != 0 or need_to_made_choice:
            not_satisfying_coalitions = []
            for c in self.other_coalitions.values():
                vote_dir = c.vote
                if vote_dir == 0:
                    vote_dir = -1
                # if debt is to small mark this as not satisfying coallition
                print("{} coalition interest {}, debt {}".format(str(self.jid), self.voters[c.sender].strength / self.strength * self.interestInApprove[self.id] * -vote_dir, c.debt))
                if self.voters[c.sender].strength/self.strength * self.interestInApprove[self.id] * -vote_dir > c.debt:
                    not_satisfying_coalitions.append(c)
                    continue
                debt += c.debt * vote_dir
                # favour when we have already debt which we should payback
                if self.voters[c.sender].debt < 0:
                    debt += -self.voters[c.sender].debt * vote_dir
            # cumulative debt is big enough to choose site
            print("{} cumulative debt {}".format(str(self.jid), debt))
            if abs(debt) > self.strength or need_to_made_choice:
                if debt > 0:
                    self.vote = 1
                else:
                    self.vote = 0
                self.generate_submit_vote()
                self.post_vote()
                return
            else:
                # we are not happy about current state, lets reject not satisfying coallitions
                # and wait for better propositions
                for c in not_satisfying_coalitions:
                    self.generate_coalition_refusal(c)

    def check_coalitions(self, budget, my_vote, possible_votes, coalitions, list_to_convince):
        for id, dist in list_to_convince:
            # base debt when proposing coalition
            debt = self.voters[id].strength / self.strength * abs(dist)
            # coalition propsed
            if id in self.my_coalitions:
                c = self.my_coalitions[id]
                # already coalition proposed or respond was positive
                if not c.responded or (c.responded and c.accept):
                    budget -= c.debt
                    # changed vote in coallition
                    if dist * my_vote[0] < 0:
                        possible_votes = 2 * self.voters[id].strength * my_vote[0]
                    continue
                # rejected proposition
                if c.responded and not c.accept:
                    # try better offer
                    new_debt = c.debt + debt * 0.2
                    # do not offer too much
                    if new_debt > debt * 2:
                        continue
                    debt = new_debt
            # id not interested in voting or vote different then us
            print("{} convince? dist {}; my_vote {}; as we? {}".format(str(self.jid), dist, my_vote[0], dist * my_vote[0]))
            if abs(dist) < self.minimal_interest or dist * my_vote[0] < 0:
                # don't have enough votes
                if possible_votes * my_vote[0] < 0 or True:
                    if debt > -self.voters[id].debt:
                        budget -= debt
                    coalitions.append(Coalition(my_vote[1], debt, self.id, id, False))
                    # may change vote in coallition
                    if dist * my_vote[0] < 0:
                        possible_votes = 2 * self.voters[id].strength * my_vote[0]

    def make_propositions(self, budget, coalitions, need_to_made_choice):
        print("{} budget after propositions {}".format(str(self.jid), budget))
        if budget > 0:
            for c in coalitions:
                self.generate_coalition_proposition(c)
        else:
            # not enough budget
            self.choose_better_propositions(need_to_made_choice)

    def make_decisions(self, need_to_made_choice=False):
        print("{} make propositions".format(str(self.jid)))
        # decision already made, accept/reject incoming coalitions
        if self.vote is not None:
            self.post_vote()
            return
        budget = abs(self.interestInApprove[self.id])
        my_vote = (1, 1) if self.interestInApprove[self.id] > 0 else (-1, 0)
        (votes_on_our_side, all_voters_strength) = self.calculate_possible_votes(my_vote)
        print("{} budget {}".format(str(self.jid), budget))
        print("{} interest in approve {}".format(str(self.jid), self.interestInApprove))
        # we think we will win, make vote
        if votes_on_our_side > all_voters_strength / 2:
            self.vote = my_vote[1]
            self.generate_submit_vote()
            self.post_vote()
            return
        # not interested in this voting, accept better coalitions
        if budget < self.minimal_interest or need_to_made_choice:
            self.choose_better_propositions(need_to_made_choice)
            return
        else:
            list_to_convince = [(id, v) for id, v in self.interestInApprove.items() if not id == self.id]
            list_to_convince.sort(key=lambda x: x[1], reverse=my_vote[0] > 0)
            coalitions = []
            possible_votes = self.calculate_possible_votes_to_convince(my_vote, list_to_convince)
            print("{} possible_votes {}".format(str(self.jid), possible_votes))
            print("{} list to convince {}".format(str(self.jid), list_to_convince))
            self.check_coalitions(budget, my_vote, possible_votes, coalitions, list_to_convince)
            self.make_propositions(budget, coalitions, need_to_made_choice)

    # This function is called when voting has not ended and no new messages are received
    def do_vote(self):
        if self.vote is None:
            print("{} Nothing changed do the vote".format(str(self.jid)))
            self.make_decisions(need_to_made_choice=True)

    @staticmethod
    def calculate_distance_to_union_state(dict_of_interest, state):
        d = 0
        for area, i in dict_of_interest.items():
            v = state.state[area]
            d += (v - i.attitude) * (v - i.attitude) * i.strength
        return sqrt(d)
