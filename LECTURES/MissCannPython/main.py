__author__ = 'giodegas'

import GameModels as G
import Heuristics as H


dicOfStates = {}

def argMin(setOfStates):
    v = []
    k = []
    for sk in setOfStates:
        #if dicOfStates.has_key(sk):
        if sk in dicOfStates:
            v += [dicOfStates[sk]]
            k += [sk]
    if len(v)>0:
        return k[v.index(min(v))]
    else:
        return None

def pick(setOfStates):
    return argMin(setOfStates)

def backpath(state):
    padre = state.parent
    lStates = [state]
    while padre!=None:
        lStates.add(padre)
        padre = padre.parent
    return reversed(lStates)

def search(game, state0):
    sHorizon = set([])
    sExplored = set([])
    sHorizon.add(state0)
    while (len(sHorizon) > 0):
        view = pick(sHorizon)
        if not (view is None):
            if game.solution(view):
                return backpath(view)
            sExplored.add(view)
            sHorizon = sHorizon | (game.neighbors(view) - sExplored)
    return None

# Main
heuristic = H.MissCannHeuristic()
game = G.MissCannGame(mr=5, cr=5, ml=0, cl=0, ship=True, shipMax=2, heuristic=heuristic)
state0 = game.getState()
dicOfStates[state0] = heuristic.H(state0)
solution = search(game, state0)
