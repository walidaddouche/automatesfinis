#!/usr/bin/env python3
"""
Read an automaton and a word, returns:
 * YES if word is recognized
 * NO if word is rejected
Determinises the automaton if it's non deterministic
"""

from typing import Set, List
from automaton import Automaton, EPSILON, State, error, warn
import sys
import pdb  # for debugging
from tp1automates import \
    is_deterministic, \
    recognizes, \
    count_element


#################
def stock_of_trans(automate: Automaton, letter: str) -> list:
    # retourne une list contenant toutes les transitions avec la lettre donné en argument
    list = []
    for i in range(len(automate.transitions)):
        if automate.transitions[i][1] == letter:
            list.append(automate.transitions[i])
    return list

def function_de_transition(automate, etat_de_depart, letter):
    try:
        return ",".join(map(lambda x: str(x), automate.statesdict[etat_de_depart].transitions
        [letter]))
    except KeyError:
        return None


def eliminate_e_trans(automate: Automaton):  # methode pour enlever les espsilon transitions d'un automate
    for l in range(len(automate.transitions)):
        while "%" in automate.transitions[l][1]:
            list_of_ep_trans = stock_of_trans(automate, "%")
            for i in range(len(list_of_ep_trans)):
                etatq = list_of_ep_trans[i][0]
                etatk = list_of_ep_trans[i][2]
                list_des_trans = []
                for k in range(len(automate.transitions)):
                    if automate.transitions[k][0] == etatk:
                        list_des_trans.append(automate.transitions[k])
                for j in range(len(list_des_trans)):
                    automate.add_transition(etatq, list_des_trans[j][1], list_des_trans[j][2])
                automate.remove_transition(etatq, "%", etatk)
                if etatk in automate.acceptstates:
                    automate.make_accept(etatq)
    for state in automate.statesdict.values():
        while function_de_transition(automate, state, "%") is not None:
            eliminate_e_trans(automate)
    automate.remove_unreachable()
    automate.name = automate.name + " sans e trans"
    return automate


##################
"TEST"
final = Automaton('final')

final.add_transition("0", "%", '1')
final.add_transition("0", "%", '3')
final.add_transition("1", "a", '1')
final.add_transition("3", "b", '3')
final.add_transition("1", "%", '2')
final.add_transition("3", "%", '4')
final.add_transition("2", "b", '2')
final.add_transition("4", "a", '4')
final.add_transition("4", "%", '5')
final.add_transition("2", "%", '5')
final.add_transition("5", "c", "5")
final.make_accept(['0', "1", "2", "3", "4", "5"])

eliminate_e_trans(final).to_graphviz("Test4/final.gv")

test6 = Automaton("test6")
test6.add_transition("0", "a", "2")
test6.add_transition("0", "a", "1")

exo2 = Automaton("det")
exo2.add_transition("0", '1', "1")
exo2.add_transition("0", '1', "0")
exo2.add_transition("0", '0', "0")
exo2.add_transition("1", '1', "2")
exo2.add_transition("2", '1', "3")

exo2.make_accept("3")


def determinise(automate: Automaton):
    automateDet = Automaton("deterministe")
    automateDet.initial = automate.initial
    listeEtats = []
    listeEtats.append(set([automate.initial.name]))
    listeEtatsNew = listeEtats
    print(listeEtats)
    while len(listeEtats) != 0:
        elt1 = listeEtats[0]
        listeEtats = listeEtats[1:]
        for elt11 in elt1:
            for x in automate.alphabet:
                EtatDest = []
                for (source, symbol, destination) in automate.transitions:
                    if source == str(elt11) and symbol == x:
                        EtatDest.append(destination)
                if (len(EtatDest) != 0) and EtatDest not in listeEtatsNew:
                    listeEtats.append(EtatDest)
                    listeEtatsNew.append(EtatDest)
                    automateDet.add_transition(str(elt1), x, str(EtatDest))
    for etat in automate.acceptstates:
        for elt1 in listeEtatsNew:
            if etat in elt1:
                automateDet.make_accept(str(elt1))
    return automateDet


test_f = Automaton('test')
test_f.add_transition("1", "a", "2")
test_f.add_transition("1", "a", "3")
test_f.add_transition("2", "a", "4")
test_f.add_transition("3", "a", "3")
test_f.add_transition("3", "b", "4")
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
        determinise(a)
    if recognizes(a, word):
        print("YES")
    else:
        print("NO")
"""""