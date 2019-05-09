from spade.behaviour import OneShotBehaviour
from spade.message import Message


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

    # async def on_end(self):
    #     await self.agent.stop()
