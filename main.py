import automaton

test = automaton.Automaton("test")


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
                elif (",".join(map(lambda x: str(x), automate.statesdict[automate.states[i]].transitions[
                    "%"]))):
                    boolean = False
            except KeyError:
                pass
    return boolean


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


test.add_transition("0", "a", "1")
test.add_transition("0", "%", "1")
test.add_transition("1", "b", "2")
test.add_transition("1", "%", "2")
test.add_transition("2", "a", "3")
test.add_transition("3", "b", "4")
test.add_transition("4", "a", "5")
test.add_transition("4", "%", "5")
test.add_transition("5", "b", "6")
test.add_transition("5", "%", "6")
test.make_accept("6")

test1 = automaton.Automaton("test")
test1.add_transition("0", "a", "1")
test1.add_transition("0", "b", "2")
test1.add_transition("0", "%", "3")
test1.add_transition("1", "a", "3")
test1.add_transition("1", "b", "2")
test1.add_transition("1", "%", "0")
test1.add_transition("2", "a", "3")
test1.add_transition("2", "b", "0")
test1.add_transition("2", "%", "1")
test1.add_transition("3", "a", "0")
test1.add_transition("3", "b", "1")
test1.add_transition("3", "%", "2")

test1.make_accept("3")
test1.to_graphviz("test1.gv")

test2 = automaton.Automaton("test2")
test2.add_transition("0", "a", "1")
test2.add_transition("0", "%", "2")
test2.add_transition("1", "b", "2")
test2.add_transition("1", "%", "4")
test2.add_transition("2", "a", "3")
test2.add_transition("2", "%", "4")
test2.add_transition("3", "b", "0")
test2.add_transition("4", "a", "2")
test2.add_transition("4", "b", "3")
test2.make_accept("3")
test2.make_accept("4")
test2.to_graphviz("test2.gv")


def stock_e_trans(
        automate: automaton.Automaton) -> list:  # retourne une liste contenant toute les epsilons transitions
    list = []
    for i in range(len(automate.transitions)):
        if automate.transitions[i][1] == "%":
            list.append(automate.transitions[i])
    return list


def stock_of_trans(automate: automaton.Automaton, etatq, lettre):
    list = []
    for i in range(len(automate.transitions)):
        if automate.transitions[i][0] == etatq and automate.transitions[i][1] == lettre:
            list.append(automate.transitions[i])
    return list


print(test1.transitions)
print(stock_of_trans(test1, "1", "b"))


def eliminate_e_trans(automate: automaton.Automaton):
    for l in range(len(automate.transitions)):
        while "%" in automate.transitions[l][1]:
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

    return automate


eliminate_e_trans(test2).to_graphviz("please2.gv")

new_states = [set([test.initial.name])]
print(str(test.initial))


def eliminate_other_trans(automate: automaton.Automaton):
    init_state = automate.initial.name
    list_of_trans_init = []
    for alphabet in automate.alphabet:
        list_of_trans_init.append(str(stock_of_trans(automate, init_state, alphabet)))
    return list_of_trans_init


def PartsOf(E):  # renvoie une liste des partie d'un ensemble
    P = [[]]
    while E:
        a = E[0]
        E = E[1:]
        Q = [x + [a] for x in P] + P
        P = Q
    P.sort()
    return P

print(PartsOf(test2.states))
a = (PartsOf(test2.states))
a.pop(0)
print(a)

test4 = automaton.Automaton("test4")
test4.add_transition("0", "a", "1")
test4.add_transition("0", "b", "2")
test4.add_transition("0", "a", "3")
test4.add_transition("1", "b", "2")
test4.add_transition("1", "a", "3")
test4.add_transition("2", "a", "3")
test4.add_transition("3", "b", "4")
test4.add_transition("4", "b", "6")
test4.add_transition("4", "a", "5")
test4.add_transition("5", "b", "6")
test4.make_accept("4")
test4.make_accept("5")
test4.make_accept("6")
test4.to_graphviz("test4.gv")
list = []
for i in range(len(test4.transitions)):
    if test4.transitions[i][0] == test4.initial.name and test4.transitions[i][1] in test4.alphabet:
        list.append(test4.transitions[i])
print(list)
lista = []
for j in range(len(list)):
    try:
        if list[j][1] == list[j + 1][1]:
            lista.append(list[j])
            lista.append(list[j + 1])
    except IndexError:
        pass
