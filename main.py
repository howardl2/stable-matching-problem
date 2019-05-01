import argparse
import os
import sys
import json


class Proposer:
    def __init__(self, name, prospects):
        self.name = name
        self.prospects = prospects
        self.current_match = None
        self.current_match_index = 0
        self.is_matched = False

    def can_match(self):
        return not self.is_matched

    def get_prospect(self):
        female_name = self.prospects[self.current_match_index]
        self.current_match_index += 1
        return female_name


class Match:
    def __init__(self, name, prospects):
        self.name = name
        self.prospects = prospects
        self.current_match = None
        self.is_matched = False

    def can_match(self):
        return not self.is_matched

    def get_preferred(self, p1, p2):
        index1 = self.prospects.index(p1)
        index2 = self.prospects.index(p2)
        return p1 if index1 < index2 else p2


class StableMatch:
    def __init__(self, males, females):
        self.male_names = list(males.keys())
        self.female_names = list(females.keys())

        self.matches = {}
        for male in males:
            self.matches[male] = Proposer(male, males[male])
        for female in females:
            self.matches[female] = Match(female, females[female])

    def match(self, male_name, female_name):
        maleObj = self.matches[male_name]
        femaleObj = self.matches[female_name]

        maleObj.is_matched = True
        femaleObj.current_match = maleObj

        femaleObj.is_matched = True
        maleObj.current_match = femaleObj

    def unmatch(self, male, female):
        maleObj = self.matches[male]
        femaleObj = self.matches[female]

        maleObj.is_matched = False
        femaleObj.current_match = None

        femaleObj.is_matched = False
        maleObj.current_match = None

    def findFreeMale(self):
        for male in self.male_names:
            if self.matches[male].can_match():
                return male
        return None

    def perform_match(self):
        while self.findFreeMale() is not None:
            male = self.matches[self.findFreeMale()]
            female = self.matches[male.get_prospect()]
            if female.can_match():
                self.match(male.name, female.name)
            else:
                male_name = female.get_preferred(male.name, female.current_match.name)
                self.unmatch(female.current_match.name, male.name)
                self.match(male_name, female.name)
        return self.matches

    def print_matches(self):
        match = {}
        for k, v in self.matches.items():
            match[k] = v.current_match.name
        print(match)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    # parser.add_argument('-payload', type=str, default="payload.json")
    # parser.add_argument('-test', default=False)
    parser.add_argument("-data", type=str, default="test.json")

    args = parser.parse_args()

    matchForm = json.load(open(args.data ,"r"))


    matching = StableMatch(matchForm["group1"], matchForm["group2"])
    matches = matching.perform_match()

    ok = lambda ok: matches != None

    matching.print_matches()

    if ok(matches):
        print("Success!")
        sys.exit(0)
    else:
        print("Failed")
        sys.exit(1)