from spade.behaviour import CyclicBehaviour

class VoteAfterTime(CyclicBehaviour):
    async def on_start(self):
        self.counter = 0

    async def run(self):
        msg = await self.receive(timeout=0.5)  # wait for a message for 0.5 seconds
        if msg:
            msg_code = msg.body.split("@")[0]
            if msg_code == "I_V_P_ev":
                self.kill()
        else:
            if self.counter < 10:
                if self.agent.has_all_data():
                    self.counter += 1
                    self.agent.make_propositions()
            else:
                self.agent.do_vote()
                self.kill()

