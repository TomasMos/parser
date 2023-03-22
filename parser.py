import nltk
import sys
from nltk.tokenize import wordpunct_tokenize
import regex as re


TERMINALS = """
Adj -> "country" | "dreadful" | "enigmatical" | "little" | "moist" | "red"
Adv -> "down" | "here" | "never"
Conj -> "and" | "until"
Det -> "a" | "an" | "his" | "my" | "the"
N -> "armchair" | "companion" | "day" | "door" | "hand" | "he" | "himself"
N -> "holmes" | "home" | "i" | "mess" | "paint" | "palm" | "pipe" | "she"
N -> "smile" | "thursday" | "walk" | "we" | "word"
P -> "at" | "before" | "in" | "of" | "on" | "to"
V -> "arrived" | "came" | "chuckled" | "had" | "lit" | "said" | "sat"
V -> "smiled" | "tell" | "were"
"""

NONTERMINALS = """
S -> NP VP | Det NP VP
NP -> N | N Det NP | P NP | N NP | Adj NP | Conj NP | N VP | Conj VP | P Det NP
VP -> V | V NP | Adv VP | Adv | V VP | Adv NP | V Det NP
"""

grammar = nltk.CFG.fromstring(NONTERMINALS + TERMINALS)
parser = nltk.ChartParser(grammar)


def main():

    # If filename specified, read sentence from file
    if len(sys.argv) == 2:
        with open(sys.argv[1]) as f:
            s = f.read()

    # Otherwise, get sentence as input
    else:
        s = input("Sentence: ")

    # Convert input into list of words
    print(s)
    s = preprocess(s)

    # Attempt to parse sentence
    try:
        trees = list(parser.parse(s))
    except ValueError as e:
        print(e)
        return
    if not trees:
        print("Could not parse sentence.")
        return

    # Print each tree with noun phrase chunks
    for tree in trees:
        tree.pretty_print()

        print("Noun Phrase Chunks")
        for np in np_chunk(tree):
            print(" ".join(np.flatten()))


def preprocess(sentence):
    """
    Convert `sentence` to a list of its words.
    Pre-process sentence by converting all characters to lowercase
    and removing any word that does not contain at least one alphabetic
    character.
    """
    list = []
    for item in wordpunct_tokenize(sentence):
        itemlower = item.lower()
        if re.search('[a-zA-Z]', itemlower):
            list.append(itemlower)
    return list



def np_chunk(tree):
    """
    Return a list of all noun phrase chunks in the sentence tree.
    A noun phrase chunk is defined as any subtree of the sentence
    whose label is "NP" that does not itself contain any other
    noun phrases as subtrees.
    """
    list = []
    grammarVar = ["NP", "VP", "S"]
    # print(tree.leaves())
    # look through all subtrees in current tree
    for subtree in tree:
        label = subtree.label()

        # check if it contains a subtree labelled NP, otherwise go to the next subtree
        if not find(subtree):
            continue

        #check if the current tree is a root node
        if label in grammarVar:
            subsub = np_chunk(subtree)
            for child in subsub:
                list.append(child)

    # print(subtree)
    if tree.label() == "NP":
        for branch in tree:
            if find(branch):
                return list
        list.append(tree)
        # print(list)

    return list




def find(tree):
    if tree.label() == "NP":
        return True
    
    if len(tree) == 1:
        return False

    for subtree in tree:
        if find(subtree):
            return True
    return False


if __name__ == "__main__":
    main()







