#!/usr/bin/env python3
"""
Read an automaton and a word, returns:
 * ERROR if non deterministic
 * YES if word is recognized
 * NO if word is rejected
"""
from typing import Union

from automaton import Automaton, EPSILON, error, warn
import sys
import pdb  # for debugging
import automaton


##################


def count_element(Word: str) -> int:
    # méthode qui compte le nombre d"états
    count = 1
    for i in range(len(Word)):
        if Word[i] == ",":
            count += 1
    return count


#########################


def is_deterministic(automate: 'Automaton') -> bool:  # Determine si un automate
    """""
    This Algo return True if the automate given is deterministe automate 
    OR
    return False if the automate is not deterministe 
    """""
    boolean = True
    for i in range(len(automate.states)):
        for j in range(len(automate.alphabet)):
            try:
                if count_element((",".join(map(lambda x: str(x), automate.statesdict
                [automate.states[i]].transitions[automate.alphabet[j]])))) > 1:
                    boolean = False
                elif (",".join(map(lambda x: str(x), automate.statesdict[automate.states[i]].
                        transitions["%"]))):
                    boolean = False
            except KeyError:
                pass
    return boolean


##################

def recognizes(a: 'Automaton', Word: str) -> bool:
    if is_deterministic(a):
        Initial_state = a.initial
        Word_inside_a_list = list(Word)
        try:
            next_state = str(Initial_state)
            for i in range(len(Word_inside_a_list)):
                if count_element((",".join(
                        map(lambda x: str(x),
                            a.statesdict[next_state].transitions[Word_inside_a_list[i]])))) == 1:
                    next_state = ",".join(
                        map(lambda x: str(x), a.statesdict[next_state].transitions[Word_inside_a_list[i]]))
                elif Word_inside_a_list[i] == "%":
                    pass
            if next_state in a.acceptstates:
                return True
            elif next_state not in a.acceptstates:
                return False
        except KeyError:
            return False
    else:
        return False

    ##################

""""
if __name__ == "__main__":
    if len(sys.argv) != 3:
        usagestring = "Usage: {} <automaton-file.af> <word-to-recognize>"
        error(usagestring.format(sys.argv[0]))

    automatonfile = sys.argv[1]
    word = sys.argv[2]

    a = Automaton("dummy")
    a.from_txtfile(automatonfile)

    if not is_deterministic(a):
        print("ERROR")
    elif recognizes(a, word):
        print("YES")
    else:
        print("NO")
"""