
from scene import *
import numpy as np
import canvas as cv
import math
import time
import json


class Sandpile:
	def __init__(self, pile, num_grains):
		self.num_grains = num_grains
		self.data = self.load_data()
		self.loops = 0
		self.prev_pile = None
		
		start = time.time()
		
		self.mat_iterate(pile)
		self.simulate(self.prev_pile)
		
		self.time_to_run = time.time() - start
		self.save_data()
		
	def mat_iterate(self, pile):
		loop = True
		while loop:
			# all cells that should topple
			mask = np.floor(pile / 4)
			pile -= 4 * mask
			pile[:, :-1] += mask[:, 1:] # left
			pile[:, 1:] += mask[:, :-1] # right
			pile[:-1, :] += mask[1:, :] # up
			pile[1:, :] += mask[:-1, :] # down
			
			self.loops += 1
			
			if not np.any(mask):
				loop = False
				self.prev_pile = pile
				
	def simulate(self, pile):
		
		pile_size = pile.shape[0]
		
		cv.set_size(pile_size*3, pile_size*3)	
		cv.begin_updates()
		
		cell_colors = [0, 1/3, 2/3, 1]
		it = np.nditer(pile, flags=['multi_index'])
		anim_s = time.time()
		
		for x in it:
			col = cell_colors[x]
			x, y = it.multi_index
			cv.set_fill_color(col, col, col)
			cv.fill_rect(x*3, y*3, 3, 3)	

		cv.end_updates()
		
		print(f'Time to render: {time.time() - anim_s}')
		center = int(pile.shape[0]/2 + .5)
		filled_center = np.nonzero(pile[center,:])
		self.d = (filled_center[0][-1] - filled_center[0][0]) + 1
		print(f'grains: {self.num_grains}')
		print(f'diameter: {self.d}')
	
	def load_data(self):
		with open('sandpile_stats.txt', 'r') as f:
			data = json.load(f)
			
		return data
				
	def save_data(self):
		self.data[f'{self.num_grains:010}'] = {'diameter': int(self.d), 'time': float(self.time_to_run)}
		
		with open('sandpile_stats.txt', 'w') as f:
			json.dump(self.data, f, indent=2, sort_keys=True)

def main():
	start_time = time.time()
	
	for i in range(10000, 100001, 10000):
		grains = i
		size = int(0.811112*(i**0.492013))
		size += 6
		if size % 2 is 0: size += 1 
		init_pile = np.zeros([size, size], dtype=np.int_)
		init_pile[size/2, size/2] = grains
		add_pile = np.zeros_like(init_pile, dtype=np.int_)
		add_pile[size/2, size/2] = 0
			
		s = Sandpile(init_pile+add_pile, grains)
		
	end_time = time.time()
	time_spent = end_time - start_time
	print(f'time spent: {time_spent}')
	

if __name__ == '__main__':
	main()
