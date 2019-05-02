

from scene import *
import math
import datetime
import json


class Simulation (Scene):
	def __init__(self, s, grains):
		super().__init__()
		self.dict_2d = s.prev_pile
		self.init_grains = grains
		
	def setup(self):
		print(f'screen size: {self.size.w} x {self.size.h}')
		self.background_color = '#3543df'
		self.cell_colors = ['#000000', 1/3, 2/3, '#ffffff']

		for k, v in self.dict_2d.items():
			x, y = k
			col = self.cell_colors[v]
			x_pos, y_pos = self.size.w/2 + 3*x, self.size.h/2 + 3*y
			
			box = SpriteNode(position=(x_pos, y_pos), x_scale=0.03, y_scale=0.03, color=col)
			self.add_child(box)
			
		self.save_pile()
		
	def save_pile(self):
		self.dict_2d = {f'{tup[0]}, {tup[1]}': val for tup, val in self.dict_2d.items()}
		
		with open(f'data_{self.init_grains}.txt', 'w') as f:
			json.dump(self.dict_2d, f, indent=2)
		
	def update(self):
		pass


class Sandpile:
	def __init__(self, pile, add_pile):
		print(f'The starting pile was: {pile}\nThe added pile was: {add_pile}\n')

		self.final_pile = self.add(pile, add_pile)
		self.prev_pile = dict(self.final_pile)
		self.itered_pile = dict(self.final_pile)
		self.loops = 0

		self.iterate()
		
	def iterate(self):
		done = 0
		loop = True
		
		while loop:
			for key, v in self.prev_pile.items():
				if v > 3:
					self.topple(key, v)
				else:
					done += 1
			
			self.loops += 1
			self.prev_pile = dict(self.itered_pile)
			
			if done == len(self.itered_pile):
				loop = False
				print(f'program loops: {self.loops}\n')
				print(f'size of pile dictionary: {len(self.itered_pile)}\n')
			done = 0
			
	def add(self, pile, add_pile):
		''' Adds corresponding cells of each pile, without toppling'''
		for k, v in add_pile.items():
			pile[k] = pile.get(k, 0) + v
		
		print(f'The two piles added together before they topple: {pile}\n')
		return pile
	
	def topple(self, key, value):
		topple_grains = math.floor(value / 4)
		x, y = key
		self.itered_pile[key] -= topple_grains * 4
		self.itered_pile[(x-1, y)] = self.itered_pile.get((x-1, y), 0) + topple_grains
		self.itered_pile[(x+1, y)] = self.itered_pile.get((x+1, y), 0) + topple_grains
		self.itered_pile[(x, y-1)] = self.itered_pile.get((x, y-1), 0) + topple_grains
		self.itered_pile[(x, y+1)] = self.itered_pile.get((x, y+1), 0) + topple_grains


def main():
	grains = 10000
	init_pile = {(0, 0): grains
	add_pile = {(0, 0): 0}

	start_time = datetime.datetime.now()
	
	s = Sandpile(init_pile, add_pile)
	run(Simulation(s, grains), show_fps=True)
	
	end_time = datetime.datetime.now()
	time_spent = end_time - start_time
	print(f'time spent: {time_spent}')
	

if __name__ == '__main__':
	main()
