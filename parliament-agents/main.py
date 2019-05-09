from agents.parliamentarianAgent import ParliamentarianAgent
from agents.votingSystemAgent import VotingSystemAgent
from agents.europeanParliamentAgent import EuropeanParliamentAgent

if __name__ == '__main__':
    agents = []
    with open("ParliamentarianAgentAccounts.txt") as f:
        content = f.readlines()
        for line in content:
            line = line.rstrip().split(" ")
            agents.append(ParliamentarianAgent(line[0], line[1], "votingSystem@jabbim.pl", None))

    votingSystem = VotingSystemAgent("votingSystem@jabbim.pl", "parlAGH123")
    votingSystem.web.start(hostname="127.0.0.1", port="10002")
    votingSystem.start()
    votingSystem.receive_message_behaviour()

    europeanParliament = EuropeanParliamentAgent("EuropeanParliamentAgent@jabbim.pl", "parlAGH123", "votingSystem@jabbim.pl")
    europeanParliament.web.start(hostname="127.0.0.1", port="10003")
    europeanParliament.start()
    europeanParliament.receive_message_behaviour()

    for parliamentarianAgent in agents:
        future = parliamentarianAgent.start()
        parliamentarianAgent.web.start(hostname="127.0.0.1", port=str(10000 + parliamentarianAgent.id))
        parliamentarianAgent.receive_message_behaviour()
        future.result()
        votingSystem.parliamentarian_agents_JIDs.append(parliamentarianAgent.jid)
        europeanParliament.parliamentarian_agents_JIDs.append(parliamentarianAgent.jid)

    votingSystem.generate_start_voting()
