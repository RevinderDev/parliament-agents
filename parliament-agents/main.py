from agents.parliamentarianAgent import ParliamentarianAgent
from agents.votingSystemAgent import VotingSystemAgent
from time import sleep

if __name__ == '__main__':
    agents = []
    with open("ParliamentarianAgentAccounts.txt") as f:
        content = f.readlines()
        for line in content:
            line = line.rstrip().split(" ")
            agents.append(ParliamentarianAgent(line[0], line[1], None))


    for parliamentarianAgent in agents:
        future = parliamentarianAgent.start()
        future.result()
        parliamentarianAgent.web.start(hostname="127.0.0.1", port=str(10000 + parliamentarianAgent.id))
        votingSystem = VotingSystemAgent("votingSystem@jabbim.pl", "parlAGH123")
        votingSystem.web.start(hostname="127.0.0.1", port="10002")
        votingSystem.start()
        while parliamentarianAgent.is_alive():
            try:
                sleep(1)
            except KeyboardInterrupt:
                parliamentarianAgent.stop()
                break


