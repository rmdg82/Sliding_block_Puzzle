# A solver for the n*n block puzzle 
# Exercise to implement various kinds of search (DFS, BFS, A*, IDA*, etc)
# Game and states classes

import copy
import random

class State:
	'''A state is a table (list of lists) where the numbers are stored in the proper order.'''
	def __init__(self,table,size,previous_actions=[]):
		self.table=table
		self.size=size
		#We use a list to store all the action we did to get to that state
		self.previous_actions=previous_actions
		
	def __eq__(self,other):
		return self.size==other.size and self.table==other.table

	def __ne__(self,other):
		return self.size!=other.size or self.table!=other.table

	def print(self):
		'''Print in a un-fashionable way the content of self.table'''
		for i in range(self.size):
			print(self.table[i])

	def print_actions(self):
		print(self.previous_actions)


class Game:
	'''Create the board as a list of lists (matrix) and initialize randomly the numbers inside it '''
	def __init__(self,size=3):
		'''Initialize the board (matrix) of size*size elements'''
		self.size=size
		#Generate a 0 filled table
		ZeroTable=[[0 for i in range(self.size)] for i in range(self.size)]
		self.state=State(ZeroTable,self.size)
		#We generate the solution table during instantiation of an obj Game
		self.SOLUTION=[]
		for row in range(self.size):
			#Create each lines and add to SOLUTION
			line=[(row)*(self.size)+j for j in range(1,self.size+1)]
			self.SOLUTION.append(line)
		self.SOLUTION[self.size-1][self.size-1]=0

		#Create a set with all the explored states of the game
		self.explored=[]

	def print(self):
		'''Print in a unfashinable way the table of self.state'''
		self.state.print()

	def print_actions(self):
		'''Print the list of previous moves'''
		self.state.print_actions()

	def set_state(self,newState):
		'''Set the newState.table as the new game.state.table.''' 
		assert self.size == newState.size , "New state length not compatible with state.size"
		copied_state=copy.deepcopy(newState)
		self.state.table=copied_state.table

	def shuffle(self,times=50):
		'''Create shuffle starting from self.SOLUTION and execute 50 random moves'''
    	#New shuffle, make 50 random moves starting from a newly create solution
		solution_list=[]
		for row in range(self.size):
			#Create each lines and add to SOLUTION
			line=[(row)*(self.size)+j for j in range(1,self.size+1)]
			solution_list.append(line)
		solution_list[self.size-1][self.size-1]=0
		#Make random choices 
		self.state=State(solution_list,self.size)
		for i in range(times):
			choosen_action=random.sample(self.valid_moves(),1)
			if choosen_action[0]=='up':
				self.up()
			elif choosen_action[0]=='down':
				self.down()
			elif choosen_action[0]=='right':
				self.right()
			elif choosen_action[0]=='left':
				self.left()
		#Clean the preavious_actions list
		self.shuffled=copy.deepcopy(self.state.previous_actions)
		self.state.previous_actions=[]
		self.explored=[]


	def up(self):
		'''Given a configuration move up the empty block (numbered 0), switching 0 and the number placed above 0.
		If not possible return False. EG:
		|1|2|3|		|1|0|3|
		|4|0|5|	=>	|4|2|5|
		|6|7|8|		|6|7|8| '''

		#Check if 0 is the first row
		if 0 in self.state.table[0]:
			return False

		#Add 'Up' to the previous_actions list
		self.state.previous_actions.append('up')
		
		#Deep copy the current state and append to game.explored before changind game.state
		copied_state=copy.deepcopy(self.state)
		self.explored.append(copied_state)

		#Find the value 0 in the last 2 rows
		for row in range(1,self.size):
			for col in range(self.size):
				if self.state.table[row][col]==0:
					#Switch the value between 0 and the number above
					value_to_switch=self.state.table[row-1][col]
					self.state.table[row][col]=value_to_switch
					self.state.table[row-1][col]=0

	def down(self):
		'''Move 0 une square down'''
		#Check if 0 is in the last row
		if 0 in self.state.table[self.size-1]:
			return False

		#Add 'Down' to the previous_actions list
		self.state.previous_actions.append('down')

		#Deep copy the current state and append to game.explored before changind game.state
		copied_state=copy.deepcopy(self.state)
		self.explored.append(copied_state)

		#Find the value 0 in the rows except the last one
		#We have to move down only the first time we enconter the 0 value and then exit. We use a count variable.
		count=0
		for row in range(self.size-1):
			for col in range(self.size):
				if (self.state.table[row][col]==0) and (count<=0):
					#Switch the value between 0 and the number below
					value_to_switch=self.state.table[row+1][col]
					self.state.table[row][col]=value_to_switch
					self.state.table[row+1][col]=0
					count +=1

	def right(self):
		'''Move 0 une square to the right'''
		#Check if 0 is in the last column
		for i in range(self.size):
			if self.state.table[i][self.size-1] == 0:
				return False

		#Add 'Right' to the previous_actions list
		self.state.previous_actions.append('right')

		#Deep copy the current state and append to game.explored before changind game.state
		copied_state=copy.deepcopy(self.state)
		self.explored.append(copied_state)

		#Find the value 0 in the all columns except the last one. Use a count var to move it only the first time we encounter the 0 value
		count=0
		for row in range(self.size):
			for col in range(self.size-1):
				if (self.state.table[row][col]==0) and (count<=0):
					#Switch he value between 0 and the number on the right
					value_to_switch=self.state.table[row][col+1]
					self.state.table[row][col]=value_to_switch
					self.state.table[row][col+1]=0
					count +=1
	
	def left(self):
		'''Move 0 une square to the left'''
		#Check if 0 is in the first column
		for i in range(self.size):
			if self.state.table[i][0] == 0:
				return False
		
		#Add 'Left' to the previous_actions list
		self.state.previous_actions.append('left')

		#Deep copy the current state and append to game.explored before changind game.state
		copied_state=copy.deepcopy(self.state)
		self.explored.append(copied_state)		

		#Find the value 0 in the all columns except the first one. Use a count var to move it only the first time we encounter the 0 value
		count=0
		for row in range(self.size):
			for col in range(1,self.size):
				if (self.state.table[row][col]==0) and (count<=0):
					value_to_switch=self.state.table[row][col-1]
					self.state.table[row][col]=value_to_switch
					self.state.table[row][col-1]=0
					count +=1
	
	def opposite(self,move):
		if move=='right':
			return 'left'
		elif move=='left':
			return 'right'
		elif move=='up':
			return 'down'
		elif move=='down':
			return 'up'
		else:
			return False

	def valid_moves(self):
		'''Given the current self.state output a list with all the possible moves among [Up,Down,Right,Left]'''
		possible_actions=set()
		#Check possible action without executing them
		#Up case
		if not 0 in self.state.table[0]:
			possible_actions.add('up')
		#Down case	
		if not 0 in self.state.table[self.size-1]:
			possible_actions.add('down')
		#Right case
		last_col=[self.state.table[i][self.size-1] for i in range(self.size)]
		if all(last_col):
			possible_actions.add('right')
		#Left case
		first_col=[self.state.table[i][0] for i in range(self.size)]
		if all(first_col):
			possible_actions.add('left')
		return possible_actions

	def check_solution(self):
		'''Check if self.state is a solution, namely equals to self.SOLUTION'''
		sol_list=[]
		for row in range(self.size):
			#Create each lines and add to SOLUTION
			line=[(row)*(self.size)+j for j in range(1,self.size+1)]
			sol_list.append(line)
		sol_list[self.size-1][self.size-1]=0

		if self.state.table == sol_list:
			return True
		else:
			return False








					

				



                
		



		

		



