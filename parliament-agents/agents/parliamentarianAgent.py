from spade.agent import Agent
from spade.behaviour import OneShotBehaviour
from spade.behaviour import CyclicBehaviour
from spade.template import Template
from spade.message import Message


class ParliamentarianAgent(Agent):
    id_count = 0

    def __init__(self, jid, password, voting_system_id, interests):
        super().__init__(jid, password)
        self.votingSystemId = voting_system_id
        self.interests = interests
        self.id = self.__class__.id_count
        self.__class__.id_count += 1

    class ReceiveBehaviour(CyclicBehaviour):
        async def run(self):
            msg = await self.receive()
            if msg:
                body = msg.body
                print("{} Message received with content: {}".format(str(self.agent.jid), body))
                if body == "I_V_P_sv":
                    self.agent.startVoting()

        async def on_end(self):
            await self.agent.stop()

    class SendBehaviour(OneShotBehaviour):
        def __init__(self, receiver, body):
            super().__init__()
            self.receiver = receiver
            self.body = body

        async def run(self):
            msg = Message(to=self.receiver)  # Instantiate the message
            msg.set_metadata("performative", "inform")  # Set the "inform" FIPA performative
            msg.body = self.body  # Set the message content
            await self.send(msg)

    async def setup(self):
        print("Parliament agent {}".format(str(self.jid)))

        # Receive (cyclic)
        b = self.ReceiveBehaviour()
        template = Template()
        template.set_metadata("performative", "inform")
        self.add_behaviour(b, template)

    def start_voting(self):
        print("{} Started voting".format(str(self.jid)))
        # b = self.SendBehaviour(msg.sender, )
        # self.add_behaviour(b)
