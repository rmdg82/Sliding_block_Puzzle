#A solver for the n*n block puzzle 
#Exercise to implement various kinds of search (DFS, BFS, A*, IDA*, etc)
#Heuristic functions, we try Manhattan distance


class Heuristics:
	'''Given a state it associates to it the estimated cost of reaching a solution from it.'''
	def __init__(self,game):
		self.size=game.size
		
		
	def manhattan_distance(self,state):
		'''Given a state return the cost calculated by the sum of the manhattan distance of every state block from the solution'''
		'''Steps:
					1)Get numbers coordinates in self.table from 1 to (self.size**2)-1
					2)Get numbers coordinates in self.solution from 1 to (self.size**2)-1, easy: 1=table[0][0], 2=table[0][1], etc
					3)Calculte the "distance" between them (easy: D(A[x][y],A[a][b])=|(x-a)|+|(y-b)|)
					4)Sum all the distances for all the number except 0.
					'''
		self.table=state.table
		cumulative_distance=0
		for num in range(1,(self.size**2)):
			#1)Get coords in self table
			row_table,col_table=int,int
			for row in range(self.size):
				if num in self.table[row]:
					row_table=row
					col_table=self.table[row].index(num)
			#2)Get coords in self.sol
			row_sol,col_sol=int,int
			row_sol=(num-1)//self.size
			col_sol=num-1-(self.size*row_sol)
			
			#3)Calculate the distance
			distance=abs(row_table-row_sol)+abs(col_table-col_sol)
			cumulative_distance+=distance
		return cumulative_distance

	def AStar_distance(self,state):
		'''Given a state (n) return a the cost given by: f(n)=g(n)+h(n).
		Where g(n) is the distance of state n from the initial state and h(n) is the manhattan distance.
		'''
		g=self.manhattan_distance(state)
		f=len(state.previous_actions)
		return g+f



