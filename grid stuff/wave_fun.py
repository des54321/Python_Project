import pygame as pg
from pygame import draw
from copy import deepcopy
from random import randint
import sys


def draw_grid(grid):
	#Das a lotta for loops
	screen.fill((0,0,0))
	grid_w = len(grid)
	grid_h = len(grid[0])
	for x in range(grid_w):
		for y in range(grid_h):
			if not grid[x][y] == -1:
				for i in range(piece_size):
					for n in range(piece_size):
						draw.rect(
						screen, colors[pieces[grid[x][y]][i][n]],
						pg.Rect(x * (s_w / grid_w) + i * (s_w / (grid_w * piece_size)),
								y * (s_h / grid_h) + n * (s_h / (grid_h * piece_size)),
								(s_w / (grid_w * piece_size)), (s_h / (grid_h * piece_size))))


def get_rules_for(grid):
	rules = []
	grid_w = len(grid)
	grid_h = len(grid[0])
	for kind in range(p_num):
		rules.append([])
		for n in range(p_num):
			for dir in l_d:
				test_all = True
				test_none = True
				for x in range(grid_w):
					for y in range(grid_h):
						if grid[x][y] == kind:
							if not input_wrap:
								if in_bounds([x + dir[0], y + dir[1]], grid_w, grid_h):
									if not grid[x + dir[0]][y + dir[1]] == n:
										test_all = False
									else:
										test_none = False
									
							else:
								ex_pos = wrap_cords([x + dir[0], y + dir[1]], grid_w, grid_h)
								if not grid[ex_pos[0]][ex_pos[1]] == n:
									test_all = False
								else:
									test_none = False




				if test_all:
					rules[kind].append(['all', dir, n])
				if test_none:
					rules[kind].append(['none', dir, n])
	
	#They told the man to stop loopin', but the man did not listen
	for kind in range(p_num):
		for n in range(p_num):
			for dir in l_d:
				if not ['none',dir,n] in rules[kind]:
					for s_dir in l_d:
						if not dir == s_dir:
							for s_n in range(p_num):
								if not ['none',s_dir,s_n] in rules[kind]:
									test = True
									for x in range(grid_w):
										for y in range(grid_h):
											if input_wrap:
												ex_pos = wrap_cords([x + dir[0], y + dir[1]], grid_w, grid_h)
												s_ex_pos = wrap_cords([x + dir[0], y + dir[1]], grid_w, grid_h)
												if grid[ex_pos[0]][ex_pos[1]] == n:
													if not grid[s_ex_pos[0]][s_ex_pos[1]] == s_n:
														test = False
														break
											else:
												if in_bounds([x + dir[0], y + dir[1]], grid_w, grid_h):
													if in_bounds([x + s_dir[0], y + s_dir[1]], grid_w, grid_h):
														if grid[x + dir[0]][y + dir[1]] == n:
															if not grid[x + s_dir[0]][y + s_dir[1]] == s_n:
																test = False
																break
										if not test:
											break
									if test:
										rules[kind].append(['if then',dir,n,s_dir,s_n])


								

	return rules


def in_bounds(pos, grid_w, grid_h):
	if pos[0] < 0:
		return False
	if pos[0] >= grid_w:
		return False
	if pos[1] < 0:
		return False
	if pos[1] >= grid_h:
		return False
	return True


def wrap_cords(pos, grid_w, grid_h):
	return [pos[0] % grid_w, pos[1] % grid_h]


def wave_func(grid_w, grid_h, rules, do_draw = False):

	grid_pos = []
	for x in range(grid_w):
		grid_pos.append([])
		for y in range(grid_h):
			add = []
			for i in range(p_num):
				add.append(i)
			grid_pos[x].append(add)

	done = False
	while not done:


		#Find each cells entropy

		entropy = []

		for x in range(grid_w):
			entropy.append([])
			for y in range(grid_h):
				entropy[x].append(len(grid_pos[x][y]))

		#Find all the cells with the lowest entropy
		pos_choice = []
		min_found = 1000
		for x in range(grid_w):
			for y in range(grid_h):
				if entropy[x][y] != 1 and entropy[x][y] != 0:
					if entropy[x][y] < min_found:
						pos_choice = []
						min_found = entropy[x][y]
						pos_choice.append([x, y])
					else:
						if entropy[x][y] == min_found:
							pos_choice.append([x, y])

		#Choose the cell to be collasped
		choice = pos_choice[randint(0, len(pos_choice) - 1)]

		#Collaspe that cell
		grid_pos[choice[0]][choice[1]] = [
		 grid_pos[choice[0]][choice[1]][randint(
		  0,
		  len(grid_pos[choice[0]][choice[1]]) - 1)]
		]

		changed = True
		while changed:
			#Make a copy so we can see if it has changed
			pre = deepcopy(grid_pos)

			#Loop through each case, see if they are happy, edit the "new" var to save

			#Understanding these ifs and loops is like quantum scienece ;)
			for x in range(grid_w):
				for y in range(grid_h):
					if not (len(grid_pos[x][y]) == 0 or len(grid_pos[x][y]) == 1):
						for n, testing in enumerate(grid_pos[x][y]):
							test = True
							for i in rules[testing]:
								if i[0] == 'none':
									if output_wrap:
										tem_pos = wrap_cords([x + i[1][0], y + i[1][1]],grid_w,grid_h)
										tem_is = grid_pos[tem_pos[0]][tem_pos[1]]
										if len(tem_is) == 1:
											if tem_is[0] == i[2]:
												test = False
									else:
										tem_pos = [x + i[1][0], y + i[1][1]]
										if in_bounds(tem_pos,grid_w,grid_h):
											tem_is = grid_pos[tem_pos[0]][tem_pos[1]]
											if len(tem_is) == 1:
												if tem_is[0] == i[2]:
													test = False
								elif i[0] == 'all':
									if output_wrap:
										tem_pos = wrap_cords([x + i[1][0], y + i[1][1]],grid_w,grid_h)
										tem_is = grid_pos[tem_pos[0]][tem_pos[1]]
										if not i[2] in tem_is:
											test = False
									else:
										tem_pos = [x + i[1][0], y + i[1][1]]
										if in_bounds(tem_pos,grid_w,grid_h):
											tem_is = grid_pos[tem_pos[0]][tem_pos[1]]
											if not i[2] in tem_is:
												test = False
								elif i[0] == 'if then':
									if output_wrap:
										tem_pos = wrap_cords([x + i[1][0], y + i[1][1]],grid_w,grid_h)
										tem_is = grid_pos[tem_pos[0]][tem_pos[1]]
										if len(tem_is) == 1:
											if tem_is[0] == i[2]:
												s_tem_pos = wrap_cords([x + i[3][0], y + i[3][1]],grid_w,grid_h)
												s_tem_is = grid_pos[s_tem_pos[0]][s_tem_pos[1]]
												if not i[4] in s_tem_is:
													test = False
									else:
										tem_pos = [x + i[1][0], y + i[1][1]]
										s_tem_pos = [x + i[3][0], y + i[3][1]]
										if in_bounds(tem_pos,grid_w,grid_h) and in_bounds(s_tem_pos,grid_w,grid_h):
											tem_is = grid_pos[tem_pos[0]][tem_pos[1]]
											if len(tem_is) == 1:
												if tem_is[0] == i[2]:
													s_tem_is = grid_pos[s_tem_pos[0]][s_tem_pos[1]]
													if not i[4] in s_tem_is:
														test = False

							if not test:
								grid_pos[x][y][n] = -1

			#Del the garbage
			for x in range(grid_w):
				for y in range(grid_h):
					n = 0
					while n < len(grid_pos[x][y]):
						if grid_pos[x][y][n] == -1:
							del grid_pos[x][y][n]
						else:
							n += 1
			if grid_pos == pre:
				changed = False
			else:
				changed = True
		test = True
		if do_draw:
			mid_grid = []
		for x in range(grid_w):
			mid_grid.append([])
			for y in range(grid_h):
				if do_draw:
					if len(grid_pos[x][y]) == 1:
						mid_grid[x].append(grid_pos[x][y][0])
					else:
						mid_grid[x].append(-1)
				if not (len(grid_pos[x][y]) == 0 or len(grid_pos[x][y]) == 1):
					test = False
		
		if do_draw:
			draw_grid(mid_grid)
			for event in pg.event.get():
				if event.type == pg.QUIT:
					sys.exit()
			
			update_pressed()
			pg.display.update()
			fps_clock.tick(fps)
		if test:
			done = True
		else:
			done = False
	final = []
	for x in range(grid_w):
		final.append([])
		for y in range(grid_h):
			if len(grid_pos[x][y]) == 1:
				final[x].append(grid_pos[x][y][0])
			else:
				final[x].append(-1)
			
	return final


pressed_letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o','p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', 'COMMA', '1', '2', '3','4', '5', '6', '7', '8', '9', '0']
pressed = []

for i in pressed_letters:
	pressed.append(False)


def update_pressed():
	global pressed
	global pressed_letters
	for x, i in enumerate(pressed_letters):
		test = 0
		pg_key = 'test = pg.K_' + i
		exec(pg_key)
		press = key_down(test)
		pressed[x] = False
		if press and (not i):
			i = True


def key_press(key: str):
	return pressed[pressed_letters.index(key)]


def key_down(key: pg.key) -> bool:
	return pg.key.get_pressed()[key]


pg.init()

#Output settings
output_wrap = False


#Looking directions
l_d = [[1, 0], [0, 1], [-1, 0], [0, -1]]
l_d = [
    [1,0],
    [1,1],
    [0,1],
    [-1,1],
    [-1,0],
    [-1,-1],
    [0,-1],
    [1,-1]
]

#Input settings


input_wrap = False
pieces = [[[0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0]], [[4, 4, 4, 4, 4, 4, 4, 2], [2, 4, 4, 2, 4, 4, 2, 2], [2, 4, 2, 2, 2, 4, 2, 2], [4, 4, 2, 2, 2, 4, 4, 4], [4, 4, 4, 2, 4, 4, 2, 2], [2, 4, 4, 4, 4, 2, 2, 2], [4, 4, 4, 4, 4, 4, 2, 2], [4, 4, 4, 4, 4, 4, 4, 4]], [[0, 0, 0, 0, 0, 0, 0, 0], [3, 3, 3, 3, 3, 3, 3, 3], [3, 0, 3, 0, 3, 0, 3, 0], [3, 0, 3, 0, 3, 0, 3, 0], [3, 0, 3, 0, 3, 0, 3, 0], [3, 0, 3, 0, 3, 0, 3, 0], [3, 3, 3, 3, 3, 3, 3, 3], [0, 0, 0, 0, 0, 0, 0, 0]], [[0, 0, 2, 4, 4, 4, 4, 4], [0, 1, 1, 1, 4, 1, 1, 4], [0, 2, 2, 1, 4, 2, 1, 4], [0, 2, 2, 1, 1, 4, 1, 4], [0, 2, 2, 1, 1, 4, 1, 4], [0, 2, 2, 1, 4, 2, 1, 4], [0, 1, 1, 1, 4, 1, 1, 4], [0, 0, 2, 4, 4, 4, 4, 4]], [[0, 0, 0, 0, 0, 0, 0, 2], [0, 0, 0, 0, 3, 0, 2, 0], [0, 0, 0, 0, 1, 3, 0, 0], [0, 0, 0, 1, 1, 1, 3, 0], [0, 0, 1, 1, 1, 0, 0, 0], [0, 1, 1, 1, 0, 0, 0, 0], [0, 1, 1, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0]]]
ex_grid = [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 3, 1, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 1, 1, 0, 0, 3, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 4, 1, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 1, 0, 0], [0, 2, 2, 2, 2, 2, 2, 2, 2, 2, 1, 0, 0, 0, 0, 0, 1, 1, 0, 0], [3, 1, 1, 0, 0, 0, 0, 0, 0, 0, 2, 2, 2, 2, 2, 2, 1, 1, 0, 0], [0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 3, 1, 1, 0, 0], [0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 2, 2, 2, 2, 2, 2, 1, 1, 0, 0], [0, 1, 1, 0, 0, 0, 0, 0, 0, 4, 1, 1, 1, 0, 0, 4, 1, 1, 0, 0], [0, 2, 2, 2, 1, 1, 0, 0, 2, 2, 1, 1, 1, 0, 0, 0, 1, 1, 0, 0], [0, 0, 0, 3, 1, 1, 0, 0, 1, 0, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 1, 1, 0, 4, 1, 0, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 1, 1, 0, 0, 1, 0, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 1, 1, 0, 0, 1, 3, 1, 1, 1, 0, 3, 1, 1, 1, 0, 0], [0, 0, 0, 0, 1, 1, 0, 0, 1, 0, 1, 1, 1, 0, 0, 1, 1, 1, 0, 0], [0, 0, 0, 4, 1, 1, 0, 0, 1, 0, 2, 2, 2, 2, 2, 1, 1, 1, 0, 0], [0, 0, 0, 0, 1, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 2, 2, 2, 2, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]]
colors = {-1: (0, 0, 0), 0: '#1C2730', 1: '#6C4E23', 2: '#535B60', 3:'#999DA8', 4: '#2D4447'}
piece_size = 8


###

p_num = len(pieces)


out_w = 30
out_h = 18
#Real width and height will be different so screen looks good
want_s_w = 1500
want_s_h = 900
s_w = (piece_size*out_w)*(want_s_w//(piece_size*out_w))
s_h = (piece_size*out_h)*(want_s_h//(piece_size*out_h))




screen = pg.display.set_mode((s_w, s_h))
fps = 60
fps_clock = pg.time.Clock()


input_rules = get_rules_for(ex_grid)
output_grid = wave_func(30, 18, input_rules,do_draw=True)

running = True
while running:

	draw_grid(output_grid)

	for event in pg.event.get():
		if event.type == pg.QUIT:
			running = False

	update_pressed()
	pg.display.update()
	fps_clock.tick(fps)
pg.quit()
