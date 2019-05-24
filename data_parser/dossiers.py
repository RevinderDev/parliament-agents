import json

parties = None

with open("../parliament-agents/resources/ParlimentParties.json") as f:
    parties = json.load(f)

with open("dossiers") as f:
    header = {}
    for i, title in enumerate(f.readline().split("|")):
        header[title.strip()] = i
    f.readline()
    for to_split in f:
        line = to_split.split("|")
        interests = {}
        for id, i in enumerate(parties[0]['interests']):
            numerator = 0
            denominator = 0
            for p in parties:
                votes_for = 0
                try:
                    votes_for = float(line[header[p['name'] + " For"]])
                except (ValueError, TypeError):
                    votes_for = 0
                weight = float(p['interests'][id]['strength']) * votes_for / float(p['size'])
                denominator += weight
                numerator += weight * float(p['interests'][id]['attitude'])
            strength = 0.05
            if denominator != 0:
                interests[i['interestArea']] = [numerator/denominator, strength]
        dossier = {}
        dossier['title'] = line[0].strip()
        dossier['subject'] = line[1].strip('\"').replace("\"\"", "\"").strip()
        dossier['reference'] = line[2].strip()
        dossier['interests'] = [ {'interestArea': k, 'attitude': v[0], 'strength': v[1]} for k, v in interests.items()]
        j = json.dumps(dossier, indent=4)
        print(j)

