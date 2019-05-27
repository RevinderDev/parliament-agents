import json

parties = None

with open("../parliament-agents/resources/ParlimentParties.json") as f:
    parties = json.load(f)

interests = {}
for id, i in enumerate(parties[0]['interests']):
    numerator = 0
    denominator = 0
    for p in parties:
        weight = float(p['size'])
        denominator += weight
        numerator += weight * float(p['interests'][id]['attitude'])
        interests[i['interestArea']] = numerator/denominator

# j = json.dumps(interests, indent=4)
# print(j)
print("[UNIONSTATE: state = [" + " ".join(["[ INTEREST_AREA_VALUE: interest_area = " + k + ", value = " + str(i) + "]" for k, i in interests.items()]) + "]]")

