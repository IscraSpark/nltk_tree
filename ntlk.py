import nltk
from nltk.tree import ParentedTree
from itertools import permutations
from fastapi import FastAPI, Query
from fastapi.responses import JSONResponse


def find_linked_nps(tree):
    linked_nps = []
    for subtree in tree.subtrees():

        if subtree.label() == 'NP':
            siblings = subtree.parent().index(subtree)

            if siblings > 0:
                prev_sibling = subtree.parent()[siblings - 1]
                prev_prev = subtree.parent()[siblings - 2]  # find pair
                if prev_sibling.label() == ',' or prev_sibling.label() == 'CC':
                    # add pair with  connector's index
                    linked_nps.append((prev_prev, prev_sibling.right_sibling(), siblings - 1))
    return linked_nps


def form_set(linked_nps):  # create set of lists of linked nps
    set_list = [[linked_nps[0][0], linked_nps[0][1]]]  # first list with a first pair

    for item in linked_nps:
        for set in set_list:
            if item[0] in set or item[1] in set:  # if one of pair in list -> second a part of combination too
                if item[0] not in set:
                    set.append(item[0])
                if item[1] not in set:
                    set.append(item[1])
            else:
                set_list.append([item[0], item[1]])  # no pair -> form next list
    return set_list


def subtree_to_str(subtree):
    sub_str = ''
    for sub in subtree:
        sub_str += str(sub)
    sub_str = sub_str.replace(')(', ') (')
    return sub_str


def swap_linked_nps(def_tree, comb, str_tree, limit=20):
    tree_list = []
    counter = 0

    for var in comb:
        parent_def = var[0][0].parent()
        str_parent_def = subtree_to_str(parent_def)

        for el in var:
            if counter == limit:
                break
            parent = parent_def.copy(True)
            for i in range(len(el)):
                parent[i * 2] = el[i].copy(True)

            str_parent = subtree_to_str(parent)
            new_val = str_tree.replace(str_parent_def, str_parent)
            tree_list.append(new_val)
            counter += 1
        if counter == limit:
            break
    return tree_list


def find_combo(lst):  # create list of combinations
    res = []
    for pos in lst:
        res.append(list(permutations(pos)))
    return res


app = FastAPI()


@app.get("/paraphrase")  # api path
def paraphrase(tree: str, limit: int = 20):

    tree_str = tree

    nltk_tree = nltk.Tree.fromstring(tree_str)
    new_tree = ParentedTree.convert(nltk_tree)

    linked_nps = find_linked_nps(new_tree)

    set_list = form_set(linked_nps)

    combos = find_combo(set_list)
    combos[0].pop(0)  # delete default combination (tree without changes)

    result = swap_linked_nps(nltk_tree, combos, tree_str, limit)
    return JSONResponse(content={"result": result})  # return result in json format

