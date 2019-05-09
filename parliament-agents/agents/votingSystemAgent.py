from spade.agent import Agent
from spade.behaviour import OneShotBehaviour
from spade.message import Message


class VotingSystemAgent(Agent):
    class SendMessageBehaviour(OneShotBehaviour):
        def __init__(self, jid, message):
            super().__init__()
            self.recipient_jid = jid
            self.message_body = message

        async def run(self):
            msg = Message(to=str(self.recipient_jid))
            msg.set_metadata("performative", "inform")
            msg.body = self.message_body
            await self.send(msg)

        async def on_end(self):
            await self.agent.stop()

    async def setup(self):
        print("Voting system agent starts")
        self.presence.set_available()

    def __init__(self, jid, password):
        super().__init__(jid, password)
        self.parliamentarian_agents_JIDs = []

    def send_message(self, recipient, message):
        if recipient == "parliamentarians":
            for jid in self.parliamentarian_agents_JIDs:
                msg_behaviour = self.SendMessageBehaviour(jid, message)
                self.add_behaviour(msg_behaviour)
