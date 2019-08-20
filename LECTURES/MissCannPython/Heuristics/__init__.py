__author__ = 'giodegas'

class Heuristic:

    def __init__(self):
        pass

    def H(self, state):
        return 1

class MissCannHeuristic(Heuristic):

    def H(self, state):
        return state.representation.mr + state.representation.cr
