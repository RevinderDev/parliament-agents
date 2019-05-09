from parliamentarianAgent import ParliamentarianAgent

agents = []
with open("ParliamentarianAgentAccounts.txt") as f:
    content = f.readlines()
    for line in content:
        line = line.rstrip().split(" ")
        agents.append(ParliamentarianAgent(line[0], line[1], None))

for parliamentarianAgent in agents:
    parliamentarianAgent.start()
    parliamentarianAgent.web.start(hostname="127.0.0.1", port=str(10000 + parliamentarianAgent.id))
    # parliamentarianAgent.stop()

