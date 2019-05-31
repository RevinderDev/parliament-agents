import json

def result_string(numerator, denominator):
    return "{0:6.2f} / {1:<6.2f} = {2:6.2f}".format(numerator, denominator, numerator/denominator)

parties = None

with open("../resources/ParlimentParties.json") as f:
    parties = json.load(f)

num = 0
dossiers = []
with open("../../data_parser/dossiers") as f:
    header = {}
    for i, title in enumerate(f.readline().split("|")):
        header[title.strip()] = i
    f.readline()
    for to_split in f:
        line = to_split.split("|")
        dossier = {}
        allVotes = 0
        forVotes = 0
        for p in parties:
            partyFor = 0
            try:
                partyFor = float(line[header[p['name'] + " For"]])
            except (ValueError, TypeError):
                partyFor = 0
            forVotes += partyFor
            allVotes += p['size']
            dossier[p['name']] = {}
            dossier[p['name']]['Total votes'] = partyFor
            dossier[p['name']]['Submitted vote'] = 1 if partyFor > p['size']/2 else 0
            dossier[p['name']]['percent for'] = partyFor / p['size']
        dossier['hasPassed'] = True if forVotes > allVotes/2 else False
        dossier['percent for'] = forVotes/allVotes
        dossier['title'] = line[0].strip()
        dossier['subject'] = line[1].strip('\"').replace("\"\"", "\"").strip()
        dossier['reference'] = str(num) + " " + line[2].strip()
        dossiers.append(dossier)
        num += 1
# j = json.dumps(dossiers, indent=4)
# print(j)
with open("voting_results_first.json") as f:
    results = json.load(f)

correct = 0
correctWeighted = 0;
correctWeightedAll = 0;

correctParty = {}
correctPartyAll = {}
correctPartyWeighted = {}
correctPartyWeightedAll = {}
for p in parties:
    correctParty[p['name']] = 0
    correctPartyAll[p['name']] = 0
    correctPartyWeighted[p['name']] = 0
    correctPartyWeightedAll[p['name']] = 0

for r in results.values():
    dossier = dossiers[int(r['id'])]
    pas = False
    if r['hasPassed'] == "True":
        pas = True
    if dossier['hasPassed'] == pas:
        correct += 1
        correctWeighted += abs(dossier['percent for'] - 0.5)
    correctWeightedAll += abs(dossier['percent for'] - 0.5)
    for p in parties:
        party_result = dossier[p['name']]
        if party_result['Submitted vote'] == r['parties choices'][p['name']]['Submitted vote']:
            correctParty[p['name']] += 1
            correctPartyWeighted[p['name']] += abs(party_result['percent for'] - 0.5)
        correctPartyAll[p['name']] += 1
        correctPartyWeightedAll[p['name']] += abs(party_result['percent for'] - 0.5)


print("Same result of voting:                 " + result_string(correct, len(results)))
print("Same result of voting (weighted):      " + result_string(correctWeighted, correctWeightedAll))
for p in parties:
    print("Same results for {:<22}".format(p['name'] + ":") + result_string(correctParty[p['name']], correctPartyAll[p['name']]))
    print("Same results for {:<22}".format(p['name'] + "(weighted):") + result_string(correctPartyWeighted[p['name']], correctPartyWeightedAll[p['name']]))
