from spade.agent import Agent
from spade.behaviour import OneShotBehaviour
from spade.message import Message


class VotingSystemAgent(Agent):
    class MessageTestBehaviour(OneShotBehaviour):

        async def run(self):
            msg = Message(to="ParliamentarianAgent1@jabbim.pl")
            msg.set_metadata("performative", "inform")
            msg.body = "Hello World"

            await self.send(msg)

        async def on_end(self):
            await self.agent.stop()

    async def setup(self):
        print("Voting system agent starts")
        self.b = self.MessageTestBehaviour()
        self.add_behaviour(self.b)

