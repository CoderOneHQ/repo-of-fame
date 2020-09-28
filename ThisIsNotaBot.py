'''
This is your AGENT. It is technically random agent but this is yours
# PLEASE don't use any additional packages other than those provided below
'''
import time
import random
import numpy as np

class agent:
	def __init__(self, player_num, env):
		self.name = "This is Not a Bot"
		self.player_num = player_num
		self.env = env

	def give_next_move(self, solid_state):
		'''
		This method is called each time the player needs to choose an 
		action
		solid_state: is a dictionary containing all the information about the board
		''' 

		#transfering a single solid_state
		self.board = solid_state["board"] 
		self.done = solid_state["done"]
		self.bombs = solid_state["bombs"]
		self.turn = solid_state["turn"]
		self.player = solid_state["players"][self.player_num-1]

		########################
		###    VARIABLES     ###
		########################

		# as player 1, the map representation of us standing on a tile with a bomb
		# is different to player 2's - so we'll store this value here for reference
		if self.player.number == 0:
			player_on_bomb_id = 6 # we are player 1
		else:
			player_on_bomb_id = 7 # we are player 2

		rows = self.board.shape[0]
		cols = self.board.shape[1] 				 

		actions = ['none','left','right','up','down','bomb']
		action_id = [0,1,2,3,4,5]
		d_actions = dict(zip(actions,action_id))

		########################
		###     HELPERS      ###
		########################

		# given a tile location as an (x,y) tuple, this function
		# will return the surrounding tiles up, down, left and to the right as a list
		# (i.e. [(x1,y1), (x2,y2),...])
		# as long as they do not cross the edge of the map
		
		# my position
		# (x,y) = self.player.position
		
		def get_surrounding_tiles(board, position):

			# store some useful information about our environment
			rows = board.shape[0]
			cols = board.shape[1]				 

			# find all the surrounding tiles relative to us
			# position[0] = row index; position[1] = col index
			tile_up = (position[0]-1,position[1]) 
			tile_down = (position[0]+1, position[1]) 		 
			tile_left = (position[0],position[1]-1)     
			tile_right = (position[0],position[1]+1)		 

			# combine these into a list
			surrounding_tiles = [tile_up, tile_down, tile_left, tile_right]

			# create a list to store tiles we can't move to
			# (ones that cross the borders of the map, and holes)
			tiles_to_remove = [] 

			for tile in surrounding_tiles:
				# i.e. that tile would go off the edge of the map
				if (tile[0] < 0 or tile[1] < 0 or tile[0] >= rows or tile[1] >= cols or 
					board[tile] == 4):
					tiles_to_remove.append(tile)

			for tile in tiles_to_remove:
				surrounding_tiles.remove(tile)

			return surrounding_tiles

		# return empty tiles 
		def get_empty_tiles(board, list_of_tiles):
		  
			# create a list for empty tiles
			empty_tiles = []

			for tile in list_of_tiles:
				if board[tile] == 0:	
					empty_tiles.append(tile)

			return empty_tiles

		# given a list of tiles, and the bomb's position on the map
		# return only the tiles which are not within 1 tile of the bomb
		def get_safe_tiles(list_of_tiles, bomb_pos):
		  
			# make a list where we'll store our safe tiles 
			safe_tiles = []

			for tile in list_of_tiles:
				# dist will give us the 'distance' to the bomb
				dist = tuple(x-y for x, y in zip(tile, bomb_pos)) 
				if dist in [(0,1),(1,0),(0,-1),(-1,0),(0,0)]:
					pass
				else:
					safe_tiles.append(tile)

			return safe_tiles

		# get surrounding tiles impacted near bomb
		def get_impacted_tiles(self, solid_state):
		
			bombs = solid_state["bombs"]

			all_impacted_tiles = []
			for bo in bombs:
				all_impacted_tiles.append(bo.impacted_tiles)
			
			return all_impacted_tiles

		# given an adjacent tile location, move us there
		def move_to_tile(position, tile):

			actions = ['none','left','right','up','down','bomb']
			action_id = [0,1,2,3,4,5]
			d_actions = dict(zip(actions,action_id))

			# see where the tile is relative to our current location
			diff = tuple(x-y for x, y in zip(position, tile))

			# return the action that moves in the direction of the tile
			if diff == (0,1):
				action = d_actions['left']
			elif diff == (1,0):
				action = d_actions['up']     
			elif diff == (0,-1):
				action = d_actions['right']     
			elif diff == (-1,0):
				action = d_actions['down']

			return action

		########################
		###      AGENT       ###
		########################

		# first, check if we've placed some bombs on the map
		if self.player.bombs:
			# if our 'player' object has bomb objects on them
			# that means we've placed a bomb, so let's run away.

			# get the bomb's position
			bomb_pos = self.player.bombs[0].position			 	

			# get a list of our surrounding tiles
			surrounding_tiles = get_surrounding_tiles(self.board, self.player.position)

			# get a list of the available tiles we can actually move to
			empty_tiles = get_empty_tiles(self.board, surrounding_tiles)	

			# get a list of the safe tiles we should move to
			safe_tiles = get_safe_tiles(empty_tiles, bomb_pos)	

			# check if we're on the bomb
			if self.board[self.player.position] == player_on_bomb_id:
				# we're on a bomb
				# let's move to an empty slot
				if empty_tiles:
					random_tile = random.choice(empty_tiles)
					action = move_to_tile(self.player.position, random_tile)
				else:
					# there aren't any empty tiles to go to
					# we're probably done for.
					action = d_actions['none']
			else:
				# we're not on a bomb
				# check if we're next to a bomb
				for tile in surrounding_tiles:
					if (tile[0] == bomb_pos[0]) and (tile[1] == bomb_pos[1]):
						# we're next to a bomb
						# move to a random safe tile (if there are any)
						if safe_tiles:
							random_tile = random.choice(safe_tiles)	
							action = move_to_tile(self.player.position, random_tile)	
							break
						else:
							# there isn't a guaranteed safe tile near us
							# choose a move at random
							action = d_actions[random.choice(actions)]
							break
				else:
					action = d_actions['none']
		
		else:
			# no bombs in play, take a random action
			action = random.choice([0,1,2,3,4,5])	

		return action