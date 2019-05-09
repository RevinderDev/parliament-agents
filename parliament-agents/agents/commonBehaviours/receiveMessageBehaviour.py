from spade.behaviour import CyclicBehaviour


class ReceiveBehaviour(CyclicBehaviour):
    async def run(self):
        msg = await self.receive()
        if msg:
            print("{} Message received with content: {}".format(str(self.agent.jid), msg.body))
            self.agent.parse_message(msg)
