#!/usr/bin/env python3
"""
Read a regular expression and returns:
 * YES if word is recognized
 * NO if word is rejected"""

from typing import Set, List
from automaton import Automaton, EPSILON, State, error, warn, RegExpReader
import sys
from tp1automates import *
from tp2automates import is_deterministic, eliminate_e_trans
from tp3automates import *
import pdb  # for debugging

##################


##################


##################


##################


##################


##################

import automaton

# ajouter vos regexp ici pour tester la conversion...

import random
import string


def get_random_string(length):
    letters = string.ascii_lowercase
    result_str = ''.join(random.choice(letters) for i in range(length))
    return result_str


def Automate_in_one_lettre(Char: str) -> automaton:
    nom = get_random_string(4)
    if Char != "%":
        nom = Automaton(nom)
        nom.add_transition("0", Char, "1")
        nom.make_accept("1")
        return nom
    else:
        nom = Automaton(str(nom))
        nom.add_transition("0", "%", "1")
        nom.make_accept("1")
        return nom


""

##################
from tp2automates import *


def regexp_to_automaton(re: str, Word: str) -> str:
    postfix = RegExpReader(re).to_postfix()
    print(postfix)
    stack: List[Automaton] = []
    for Element in postfix:
        pdb.set_trace()
        if Element != '+' and \
                Element != "*" and \
                Element != '.':
            Element = Automate_in_one_lettre(Element)
            stack.append(Element)
        elif Element == '+':
            left = stack.pop()
            right = stack.pop()
            stack.append(union(right, left))
        elif Element == '.':
            right = stack.pop()
            left = stack.pop()
            stack.append(concat(right, left))
        elif Element == "*":
            a = stack.pop()
            stack.append(a)
    stack[0].name = "result"
    stack[0].to_graphviz("Test1/test.gv")
    stack[0] = eliminate_e_trans(stack[0])
    stack[0].to_graphviz("Test1/test1.gv")

    if recognizes(stack[0], Word):
        return "YES"
    else:
        return "NO"


a1 = Automate_in_one_lettre("a")
a2 = Automate_in_one_lettre("b")

print((regexp_to_automaton("ab", "ab")))
##################

"""if __name__ == "__main__":

    if len(sys.argv) != 3:
        usagestring = "Usage: {} <regular-expression> <word-to-recognize>"
        error(usagestring.format(sys.argv[0]))

    regexp = sys.argv[1]
    word = sys.argv[2]

    a = regexp_to_automaton(regexp)
    determinise(a)
    if recognizes(a, word):
        print("YES")
    else:
        print("NO")
"""
