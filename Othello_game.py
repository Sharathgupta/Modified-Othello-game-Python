#!/usr/bin/python

import sys

#Open File
fp = open(sys.argv[-1],'r')
type_of_algo = int((fp.readline()).strip())
if type_of_algo == 4:
	player = (fp.readline()).strip()
	player_algo = int((fp.readline()).strip())
	player_depth = int((fp.readline()).strip())
	opponent = (fp.readline()).strip()
	opponent_algo = int((fp.readline()).strip())
	opponent_depth = int((fp.readline()).strip())

else:
	player_algo = type_of_algo
	player = (fp.readline()).strip()
	player_depth = int((fp.readline()).strip())
	max_i = 0
	max_j = 0
	current_gain = 0
	opponent = 'X'
	if player == 'X':
		opponent = 'O'

matrix = []
for i in range(5):
	matrix.append((fp.next()).split())
board = [list(line.strip()) for line in fp]

fp.close()


def compute(board):
	current_player_value = 0
	current_opponent_value = 0
	for i in range(5):
		for j in range(5):
			if board[i][j] == player:
				current_player_value += int(matrix[i][j])
			elif board[i][j] == opponent:
				current_opponent_value += int(matrix[i][j])
	return current_player_value-current_opponent_value

def israid(board,i,j,player,opponent):
	raid = False
	if i>0 and board[i-1][j] == player:
		raid = True
	elif j>0 and board[i][j-1] == player:
		raid = True
	elif i<4 and board[i+1][j] == player:
		raid = True
	elif j<4 and board[i][j+1] == player:
		raid = True
	return raid

def changeboard(board,i,j,player,opponent):
	next_board = [row[:] for row in board]
	next_board[i][j] = player
	if israid(next_board,i,j,player,opponent):
		if i>0 and next_board[i-1][j] == opponent:
			next_board[i-1][j]	= player
		if j>0 and next_board[i][j-1] == opponent:
			next_board[i][j-1] = player
		if i<4 and next_board[i+1][j] == opponent:
			next_board[i+1][j] = player
		if j<4 and next_board[i][j+1] == opponent:
			next_board[i][j+1] = player
	return next_board

def num_of_stars(board):
	count = 0
	for i in range(5):
		for j in range(5):
			if board[i][j] == '*':
				count = count + 1
	return count

def print_traverse(i,j,counter,val,alpha,beta):
	if type_of_algo == 4:
		return
	if i==-2:
		traverse_log.write("Node,Depth,Value")	
	elif i==-1 and j ==-1:
		if val == sys.maxint:
			traverse_log.write('root,'+ str(counter) + ',Infinity')
		elif val == -sys.maxint-1:
			traverse_log.write('root,'+str(counter) +',-Infinity')
		else:
			traverse_log.write('root,'+str(counter) + ',' + str(val))
		
	else:
		if val == sys.maxint:
			traverse_log.write(chr(ord('A')+j) + str(i+1)+',' + str(counter) + ',Infinity')
		elif val == -sys.maxint -1:
			traverse_log.write(chr(ord('A')+j)+ str(i+1) +','+ str(counter) + ',-Infinity')
		else:
			traverse_log.write(chr(ord('A')+j) + str(i+1) +','+ str(counter) + ','+str(val))
	
	if type_of_algo == 3:
		if i == -2:
			traverse_log.write(',Alpha,')
		elif alpha == -sys.maxint-1:
			traverse_log.write(',-Infinity,')
		else:
			traverse_log.write(',' + str(alpha) + ',')

		if i == -2:
			traverse_log.write('Beta\n')
		elif beta == sys.maxint:
			traverse_log.write('Infinity\n')
		else:
			traverse_log.write(str(beta) + '\n')

	else:
		traverse_log.write('\n')
	
def callmax(counter, board, i, j, alpha, beta, algo, depth):
	max_val = -sys.maxint - 1
	cur_val = 0
	cur_i = 0
	cur_j = 0
	counter = counter + 1
		
	temp_board = changeboard(board,i,j,opponent,player)
	if(counter == depth or num_of_stars(temp_board) == 0):
		max_val =  compute(temp_board)
		if (type_of_algo == 2 or type_of_algo ==3):
			print_traverse(i,j,counter,max_val,alpha,beta)
		return max_val,i, j
	else:
		if (type_of_algo == 2 or type_of_algo ==3):
			print_traverse(i,j,counter,max_val,alpha,beta)
		for x in range(5):
			for y in range(5):
				if(temp_board[x][y] == '*'):
					cur_val, cur_i, cur_j = callmin(counter, temp_board, x, y, alpha, beta)
					if cur_val > max_val:
						max_i = cur_i
						max_j = cur_j
						max_val = cur_val
					if type_of_algo == 3:
						if max_val >= beta:
							print_traverse(i,j,counter,max_val,alpha,beta)
							return max_val, max_i, max_j
						alpha = max(alpha, max_val)
					if (type_of_algo == 2 or type_of_algo ==3):
						print_traverse(i,j,counter,max_val,alpha,beta)
		return max_val, max_i, max_j
	
def callmin(counter, board, i, j, alpha, beta, algo, depth):
	min_val = sys.maxint
	cur_val = 0
	cur_i = 0
	cur_j = 0
	counter = counter + 1
	temp_board = changeboard(board,i,j,player,opponent)
	if(counter == depth or num_of_stars(temp_board) == 0):
		min_val = compute(temp_board)
		if (algo == 2 or algo ==3):
			print_traverse(i,j,counter,min_val,alpha,beta)
		return min_val, i, j
	else:
		if (algo == 2 or algo ==3):
			print_traverse(i,j,counter,min_val,alpha,beta)
		for x in range(5):
			for y in range(5):
				if(temp_board[x][y] == '*'):
					cur_val, cur_i, cur_j = callmax(counter, temp_board, x, y, alpha, beta, algo, depth)
					if cur_val < min_val:
						min_i = cur_i
						min_j = cur_j
						min_val = cur_val
					if algo == 3:
						if min_val <= alpha:
							print_traverse(i,j,counter,min_val,alpha,beta)
							return min_val, min_i, min_j
						beta = min(beta, min_val)
					if (algo == 2 or algo ==3):
						print_traverse(i,j,counter,min_val,alpha,beta)
		return min_val, min_i, min_j
	
def all_algos(board,algo,depth):
	counter = 0
	max_val = -sys.maxint-1
	cur_val = 0
	alpha = -sys.maxint-1
	beta = sys.maxint
	if (algo == 2 or algo ==3):
		print_traverse(-2,-2,counter,max_val,alpha,beta)
		print_traverse(-1,-1,counter,max_val,alpha,beta)
	for i in range(5):
		for j in range(5):
			if(board[i][j] == '*'):
				cur_val, cur_i, cur_j = callmin(counter, board, i, j, alpha, beta, algo, depth)
				if cur_val > max_val:
					max_i = i
					max_j = j
					max_val = cur_val
				alpha = max_val
				if (algo == 2 or algo ==3):
					print_traverse(-1,-1,counter,max_val,alpha,beta)
	final_board = changeboard(board, max_i, max_j, player, opponent)
	return final_board

def print_state(board):
	for i in range(5):
		for j in range(5):
			trace.write(board[i][j])
		trace.write('\n')	
if (type_of_algo == 2 or type_of_algo ==3):
	traverse_log = open('traverse_log.txt','w')

if type_of_algo < 4:
	print_board = all_algos(board,player_algo,player_depth)
	f = open('next_state.txt','w')
	for i in range(5):
		for j in range(5):
			f.write(print_board[i][j])
		f.write('\n')	

else:
	trace = open('trace_state.txt','w')
	change_board = [row[:] for row in board]
	while(num_of_stars(change_board) != 0):
		change_board = all_algos(change_board,player_algo,player_depth)
		player,opponent = opponent,player
		print_state(change_board)
		if(num_of_stars(change_board) == 0):
			break
		change_board = all_algos(change_board,opponent_algo,opponent_depth)
		player,opponent = opponent,player
		print_state(change_board)	


if (type_of_algo == 2 or type_of_algo ==3):
	traverse_log.close()

if (type_of_algo == 4):
	trace.close()
