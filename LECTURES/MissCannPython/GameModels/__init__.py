__author__ = 'giodegas'

class MissCannRepresentation:

    def __init__(self, mr, cr, ml, cl, ship):
        self.mr = mr
        self.cr = cr
        self.ml = ml
        self.cl = cl
        self.ship = ship

    def isAmmissible(self):
        return (self.cl<=self.ml) and (self.cr<=self.mr)

class MissCannState:

    def __init__(self, parent, mr, cr, ml, cl, ship, heuristic):
        self.parent = parent
        self.H = heuristic
        self.representation = MissCannRepresentation(mr, cr, ml, cl, ship)

class Game:

    def __init__(self, initialState=None, heuristic=None):
        self.state = initialState
        self.heuristic = heuristic

    def neighbors(self, state):
        out = set([])
        return out

    def getState(self):
        return self.state

    def solution(self, state):
        return True

class MissCannGame(Game):

    def __init__(self, mr, cr, ml, cl, ship, shipMax, heuristic):
        self.state = MissCannState(None, mr, cr, ml, cl, ship, heuristic)
        self.shipMax = shipMax

    def neighbors(self, state):
        out = set([])
        rep = state.representation
        if rep.ship: # True a sinistra
            for m in range(0,self.shipMax+1):
                for c in range(0, self.shipMax-m):
                    if (m <= rep.mr) and (c <= rep.cr):
                        n = MissCannRepresentation(rep.mr+m, rep.cr+c, rep.ml-m, rep.cl-c, not rep.ship)
                        if n.isAmmissible():
                            n.parent = state
                            out.add(n)
        else:
            for m in range(0,self.shipMax+1):
                for c in range(0, self.shipMax-m):
                    if (m <= rep.ml) and (c <= rep.cl):
                        n = MissCannRepresentation(rep.mr-m, rep.cr-c, rep.ml+m, rep.cl+c, not rep.ship)
                        if n.isAmmissible():
                            n.parent = state
                            out.add(n)
        return out

    def solution(self, state):
        out = (state.representation.mr == 0) and (state.representation.cr == 0)
        return out