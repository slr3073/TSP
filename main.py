import math
import random
from copy import copy
import time

t0 = time.time()

def trunc2(i):
    return math.trunc(i * 100) / 100

def read(file):
    r = []
    with open(file) as f:
        content = f.readlines()
        content.pop(0)
        for line in content:
            lineVals = line.split('\t')
            r.append({"num": int(lineVals[0]), "x": int(lineVals[1]), "y": int(lineVals[2][0:len(lineVals[2]) - 1])})
    return r

def distance(v1, v2):
    return math.sqrt((v1["x"] - v2["x"]) ** 2 + (v1["y"] - v2["y"]) ** 2)

def rdmSol(sol):
    random.shuffle(sol)
    return sol

def distSol(sol):
    res = distance({"x": 0, "y": 0}, sol[0])
    for i in range(len(sol) - 1):
        res += distance(sol[i], sol[i + 1])
    res += distance(sol[len(sol) - 1], {"x": 0, "y": 0})
    return res

def solNums(sol):
    return [v["num"] for v in sol]

def meilleur_voisin(sol):
    permTodo = [(i, j) for i in range(len(sol)) for j in range(len(sol)) if j > i]

    best = copy(sol)
    f_perm = permTodo.pop(0)
    best[f_perm[0]], best[f_perm[1]] = best[f_perm[1]], best[f_perm[0]]
    bestVal = distSol(best)

    for perm in permTodo:
        voisin = copy(sol)
        voisin[perm[0]], voisin[perm[1]] = voisin[perm[1]], voisin[perm[0]]
        distVoisin = distSol(voisin)
        if distVoisin < bestVal:
            bestVal = distVoisin
            best = voisin

    return best

def meilleur_voisin_non_tabou(sol, tabou):
    permTodo = [(i, j) for i in range(len(sol)) for j in range(len(sol)) if j > i]
    best = copy(sol)
    f_perm = permTodo.pop(0)
    best[f_perm[0]], best[f_perm[1]] = best[f_perm[1]], best[f_perm[0]]
    bestVal = distSol(best)

    for perm in permTodo:
        voisin = copy(sol)
        voisin[perm[0]], voisin[perm[1]] = voisin[perm[1]], voisin[perm[0]]
        distVoisin = distSol(voisin)
        if distVoisin < bestVal and voisin not in tabou:
            bestVal = distVoisin
            best = voisin

    if best == sol:
        print("lol")
        return None
    return best

def voisins(sol):
    res = []
    permTodo = [(i, j) for i in range(len(sol)) for j in range(len(sol)) if j > i]
    for perm in permTodo:
        voisin = copy(sol)
        voisin[perm[0]], voisin[perm[1]] = voisin[perm[1]], voisin[perm[0]]
        res.append(voisin)
    return res

def hill_climbing_try(sol):
    rdmSolu = rdmSol(sol)
    res = {"init": rdmSolu, "msol": rdmSolu, "nb_depl": 0}

    while True:
        res["nb_depl"] += 1
        new = meilleur_voisin(res["msol"])
        if distSol(res["msol"]) <= distSol(new):
            break
        res["msol"] = new

    print("init : ", trunc2(distSol(res["init"])), "| msol : ", trunc2(distSol(res["msol"])), "| nb_depl : ",
          res["nb_depl"])
    return res

def steepest_hill_climbing(data, nb_try):
    res = hill_climbing_try(data)
    for i in range(1, nb_try):
        essais = hill_climbing_try(data)
        if distSol(essais["msol"]) < distSol(res["msol"]):
            res = essais
    return res

def tabou_algo(data, MAX_depl, tabou_size):
    res = {"init": data, "s": data, "msol": data, "nb_depl": 0, "tabou": []}
    while res["nb_depl"] < MAX_depl:
        sp = meilleur_voisin_non_tabou(res["s"], res["tabou"])
        if sp is None:
            break
        if len(res["tabou"]) == tabou_size:
            res["tabou"].pop(0)
        res["tabou"].append(res["s"])
        if distSol(sp) < distSol(res["msol"]):
            res["msol"] = sp
            print(distSol(sp))
        res["s"] = sp
        res["nb_depl"] += 1
    return res

resu = steepest_hill_climbing(read("tsp101.txt"), 10)
print(resu["init"], "")
print(trunc2(distSol(resu["msol"])), "in ", trunc2(time.time() - t0), "s")

print(distSol(tabou_algo(resu["init"], 250, 50)["msol"]), "in ", trunc2(time.time() - t0), "s")



