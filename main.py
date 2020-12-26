from typing import Union
import automaton
from Automate_test import *


def count_element(Word: str) -> int:  # méthode qui compte le nombre d"état
    count = 1
    for i in range(len(Word)):
        if Word[i] == ",":
            count += 1
    return count


def is_det(automate: automaton.Automaton) -> bool:  # Determine si un automate
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


def is_word_inside(automate: automaton.Automaton, mot: str) -> Union[bool, str]:
    """
    RETURN TRUE IF THE WORD GIVEN IS RECOGNIZE BY THE AUTOMATON
    OR
    FALSE IF THE THE WORD IS NOT RECOGNIZE
    """

    if is_det(automate):
        Initial_state = automate.initial
        Word_inside_a_list = list(mot)
        try:
            next_state = str(Initial_state)
            for i in range(len(Word_inside_a_list)):
                if count_element((",".join(
                        map(lambda x: str(x),
                            automate.statesdict[next_state].transitions[Word_inside_a_list[i]])))) == 1:
                    next_state = ",".join(
                        map(lambda x: str(x), automate.statesdict[next_state].transitions[Word_inside_a_list[i]]))
                elif Word_inside_a_list[i] == "%":
                    pass
            if next_state in automate.acceptstates:
                return True
            elif next_state not in automate.acceptstates:
                return False
        except KeyError:
            return False
    else:
        return "ERROR \n votre automate n'est pas un atomate déterministe "


def final_method(path_to_file: str, Word: str) -> str:
    Auto = automaton.Automaton("test")  # create an empty automate
    Auto.from_txtfile(path_to_file)
    if not is_det(Auto):
        return "ERROR"
    else:
        if is_word_inside(Auto, Word):
            return "YES"
        else:
            return "NO"


def stock_e_trans(automate: automaton.Automaton) -> list:  # retourne une liste contenant toute les epsilons transitions
    list = []
    for i in range(len(automate.transitions)):
        if automate.transitions[i][1] == "%":
            list.append(automate.transitions[i])
    return list


def stock_of_trans(automate: automaton.Automaton, etatq, lettre) -> list:
    list = []
    for i in range(len(automate.transitions)):
        if automate.transitions[i][0] == etatq and automate.transitions[i][1] == lettre:
            list.append(automate.transitions[i])
    return list


def PartsOf(E: list):  # renvoie une liste des partie d'un ensemble
    P = [[]]
    while E:
        a = E[0]
        E = E[1:]
        Q = [x + [a] for x in P] + P
        P = Q
    P = sorted(P)
    return P


def Transition_Function(automate, Initial_state, letter):
    return ",".join(map(lambda x: str(x), automate.statesdict[Initial_state].transitions[
        letter]))


def eliminate_other_trans(automate: automaton.Automaton) -> automaton:  # Methode incompléte
    automate = eliminate_e_trans(automate)
    new_state = [automate.initial.name]
    PartsOf(automate.states)
    resulting_automaton = automaton.Automaton("test4")
    for i in range(len(automate.alphabet)):
        try:
            etat_cible = Transition_Function(automate, automate.initial.name, automate.alphabet[i])
            new_state.append(str(etat_cible))
            resulting_automaton.add_transition(automate.initial.name, automate.alphabet[i], etat_cible)
        except KeyError:
            pass
    for i in range(len(automate.alphabet)):
        print(new_state[2][2])
        print(Transition_Function(automate, new_state[1][0], automate.alphabet[i]))

    return resulting_automaton


def eliminate_e_trans(
        automate: automaton.Automaton) -> automaton:  # methode pour enlever les espsilon transitions d'un automate
    try:
        for l in range(len(automate.transitions)):
            list_of_ep_trans = stock_e_trans(automate)
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
        while not stock_e_trans(automate) == False:
            eliminate_other_trans(automate)
    finally:
        return automate


eliminate_e_trans(test1).to_graphviz("test11.gv")
