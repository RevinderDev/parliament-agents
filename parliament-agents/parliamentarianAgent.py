from spade.agent import Agent
from spade.behaviour import OneShotBehaviour
from spade.message import Message
from spade.template import Template


class ParliamentarianAgent(Agent):
    id_count = 0

    def __init__(self, jid, password, interests):
        super().__init__(jid, password)
        self.interests = interests
        self.id = self.__class__.id_count
        self.__class__.id_count += 1

    class RecvBehav(OneShotBehaviour):
        async def run(self):
            print("RecvBehav running")
            msg = await self.receive(timeout=10)  # wait for a message for 10 seconds
            if msg:
                print("Message received with content: {}".format(msg.body))
            else:
                print("Did not received any message after 10 seconds")
            # stop agent from behaviour
            self.agent.stop()

    def setup(self):
        print("Agent {}".format(str(self.jid)))
        print("ReceiverAgent started")
        b = self.RecvBehav()
        template = Template()
        template.set_metadata("performative", "inform")
        self.add_behaviour(b, template)

