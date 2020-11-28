#!/usr/bin/env python3
"""
Read an automaton and a word, returns:
 * ERROR if non deterministic
 * YES if word is recognized
 * NO if word is rejected
"""

import automaton
import sys
import pdb  # for debugging

if len(sys.argv) != 3:
    usagestring = "Usage: {} <automaton-file.af> <word-to-recognize>"
    automaton.error(usagestring.format(sys.argv[0]))

import automaton
import sys

test = automaton.Automaton("Test")  # create a empty automate
test.add_transition("0", "b", "1")
test.add_transition("1", "b", "1")
test.add_transition("1", "a", "2")
test.add_transition("2", "b", "2")

test.make_accept("2")
test.to_graphviz("test.gv")


def count_element(Word: str):  # méthode qui compte le nombre d"état
    count = 1
    for i in range(len(Word)):
        if Word[i] == ",":
            count += 1
    return count


def is_det(automate: automaton.Automaton):
    boolean = True
    for i in range(len(automate.states)):
        for j in range(len(automate.alphabet)):
            try:
                if count_element((",".join(map(lambda x: str(x), automate.statesdict[automate.states[i]].transitions[
                    automate.alphabet[j]])))) > 1:
                    boolean = False
                elif count_element((",".join(map(lambda x: str(x), automate.statesdict[automate.states[i]].transitions[
                    "%"])))) > 1:
                    boolean = False
            except KeyError:
                pass
    return boolean


print(is_det(test))


def is_word_inside(automate: automaton.Automaton, mot: str):
    if is_det(automate):
        etat_initiale = automate.initial
        lista = list(mot)
        try:
            etat_suivant = str(etat_initiale)
            for i in range(len(lista)):
                if count_element((",".join(
                        map(lambda x: str(x), automate.statesdict[etat_suivant].transitions[lista[i]])))) == 1:
                    etat_suivant = ",".join(
                        map(lambda x: str(x), automate.statesdict[etat_suivant].transitions[lista[i]]))
                elif lista[i] == "%":
                    pass
            if etat_suivant in automate.acceptstates:
                return True
            elif etat_suivant not in automate.acceptstates:
                return False
        except KeyError:
            return False
    else:
        return "ERROR \n votre automate n'est pas un atomate déterministe "


def final_method(chemin_vers_le_fichier: str, Word: str):
    Auto = automaton.Automaton("test")  # create an empty automate
    Auto.from_txtfile(chemin_vers_le_fichier)
    if not is_det(Auto):
        return "ERROR"
    else:
        if is_word_inside(Auto, Word):
            return "YES"
        else:
            return "NO"


automatonfile = sys.argv[1]
word = str(sys.argv[2])
print(final_method(automatonfile, word))

# mot = input("le mot que vous chechez")
# chemin = input("le chemin vers l'automate")
# print(final_method(chemin,mot))&
