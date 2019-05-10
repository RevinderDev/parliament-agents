from spade.behaviour import CyclicBehaviour


class ReceiveBehaviour(CyclicBehaviour):
    async def run(self):
        msg = await self.receive()
        if msg:
            print("{} Message received with content: {} from {}".format(str(self.agent.jid), msg.body, msg.sender))
            self.agent.parse_message(msg)
