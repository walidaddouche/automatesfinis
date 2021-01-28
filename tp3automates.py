#!/usr/bin/env python3
"""
Applies Kleene's star, concatenation and union of automata.
"""

from automaton import Automaton, EPSILON, State, error, warn
import sys
import pdb  # for debugging


def nouvel_etat(a1: Automaton) -> str:
    """Trouve un nouveau nom d'état supérieur au max dans `a1`"""
    maxstate = -1
    for a in a1.states:
        try:
            maxstate = max(int(a), maxstate)
        except ValueError:
            pass  # ce n'est pas un entier, on ignore
    return str(maxstate + 1)


##################

def kleene(a1: Automaton) -> Automaton:
    a2 = a1.deepcopy()
    for state in a2.acceptstates:
        a2.add_transition(state, "%", a2.initial.name)
    new_initial_state = nouvel_etat(a1)
    a2.add_transition(new_initial_state, EPSILON, a1.initial.name)
    a2.initial = a2.statesdict[new_initial_state]
    a2.make_accept(new_initial_state)
    a2.name = "kleen"
    return a2

    ##################


def concat(a1: Automaton, a2: Automaton) -> Automaton:
    a1star_a2 = a1.deepcopy()
    a1star_a2.name = "a1star_a2"
    nom_nouvel_etat = nouvel_etat(a1star_a2)
    for s in a2.states:
        if s in a1star_a2.states:  # l'état de a2 existe dans la copie de a1star
            a2.rename_state(s, nom_nouvel_etat)  # ici on modifie a2 directement -> à éviter
            nom_nouvel_etat = str(int(nom_nouvel_etat) + 1)  # incrémente le compteur
    for (s, a, d) in a2.transitions:
        a1star_a2.add_transition(s, a, d)
    a1star_a2.make_accept(a2.acceptstates)
    for ac in a1.acceptstates:
        a1star_a2.add_transition(ac, EPSILON, a2.initial.name)
    a1star_a2.make_accept(a1.acceptstates, accepts=False)  # transforme en états non acceptants

    return a1star_a2


##################


def union(a1: Automaton, a2: Automaton) -> Automaton:
    Union = a1.deepcopy()
    nom_nouvel_etat = nouvel_etat(a2)
    for s in a2.states:
        if s in Union.states:
            Union.rename_state(s, nouvel_etat(a2))  # ici on modifie a3 directement -> à éviter
            nom_nouvel_etat = str(int(nom_nouvel_etat) + 1)
    for (s, a, d) in a2.transitions:
        Union.add_transition(s, a, d)
    Union.make_accept(a2.acceptstates)
    Union.add_transition(nom_nouvel_etat, EPSILON, a1.initial.name)
    Union.add_transition(nom_nouvel_etat, EPSILON, a2.initial.name)
    Union.initial.name = nom_nouvel_etat
    Union.remove_transition(Union.initial.name, EPSILON, Union.initial.name)
    return Union


def TestTP():
    a1 = Automaton("dummy")
    a1.from_txtfile("test/a.af")
    a2 = Automaton("dummy1")
    a2.from_txtfile("test/b.af")
    a1.to_graphviz(a1.name + ".gv")
    a2.to_graphviz(a2.name + ".gv")
    print(a1)
    print(a2)
    print(concat(a1, a2))
    a1star = kleene(a1)
    print()
    print(a1star)
    a1star.to_graphviz("a1star.gv")

    a1a2 = concat(a1, a2)
    print()
    print(a1a2)
    a1a2.to_graphviz("a1a2.gv")

    a1ora2 = union(a1, a2)
    print()
    print(a1ora2)
    a1ora2.to_graphviz("a1ora2.gv")


TestTP()

##################
""""
if __name__ == "__main__":
    if len(sys.argv) != 3:
        usagestring = "Usage: {} <automaton-file1.af> <automaton-file2.af>"
        error(usagestring.format(sys.argv[0]))

    # First automaton, argv[1]
    a1 = Automaton("dummy")
    a1.from_txtfile(sys.argv[1])
    a1.to_graphviz(a1.name + ".gv")
    print(a1)

    # Second automaton, argv[2]
    a2 = Automaton("dummy")
    a2.from_txtfile(sys.argv[2])
    a2.to_graphviz(a2.name + ".gv")
    print(a2)

    a1star = kleene(a1)
    print()
    print(a1star)
    a1star.to_graphviz("a1star.gv")

    a1a2 = concat(a1, a2)
    print()
    print(a1a2)
    a1a2.to_graphviz("a1a2.gv")

    a1ora2 = union(a1, a2)
    print()
    print(a1ora2)
    a1ora2.to_graphviz("a1ora2.gv")
"""
