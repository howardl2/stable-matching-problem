import argparse
import os
import sys
import json

PAYLOAD_ENV = "PAYLOAD_JSON"

def stableMatch(matchForm):
    groups = list(matchForm.keys())
    if len(groups) > 2:
        return None
    group1 = groups[0]
    group2 = groups[1]

    trackMatches = {}
    # choose group1
    for client in matchForm[group1].keys():
        print()
        print(client)
        trackMatches[client] = None # setup the client
        for potential in matchForm[group1][client]:
            if not trackMatches[client]:
                # first pass
                trackMatches[client] = potential

    print()

    return {}


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='JetFire - transcode your way.')
    # parser.add_argument('-payload', type=str, default="payload.json")
    # parser.add_argument('-test', default=False)
    parser.add_argument("-data", type=str, default="test.json")

    args = parser.parse_args()

    matchForm = json.load(open(args.data ,"r"))
    matches = stableMatch(matchForm)

    ok = lambda ok: matches != None

    if ok(matches):
        print("Success!")
        sys.exit(0)
    else:
        print("Failed")
        sys.exit(1)