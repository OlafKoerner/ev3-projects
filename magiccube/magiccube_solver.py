
from magiccube.magiccube_main import RUN_ON_EV3
#import msvcrt as ms
import numpy as np
if not RUN_ON_EV3:
    import matplotlib
    matplotlib.use('TkAgg')
    import matplotlib.pyplot as plt
    #import platform
    #if platform.system() == 'Darwin':
    #   matplotlib.use('MacOSX')
    from mpl_toolkits.mplot3d import Axes3D
    from mpl_toolkits.mplot3d.art3d import Poly3DCollection, Line3DCollection

import time as t
from inspect import currentframe
import magiccube_device as mcd



ERR_ACTION_EXIT = 1

FACE_SIZE = 0.4

SIDE_DIR_RED = (0, 1, 0)
SIDE_COL_RED = 'r'
SIDE_DIR_ORANGE = (0, -1, 0)
SIDE_COL_ORANGE = 'c' # [1.0, 0.4, 0.0]
SIDE_DIR_YELLOW = (0, 0, 1)
SIDE_COL_YELLOW = 'y'
SIDE_DIR_WHITE = (0, 0, -1)
SIDE_COL_WHITE = 'w'
SIDE_DIR_GREEN = (-1, 0, 0)
SIDE_COL_GREEN = 'g'
SIDE_DIR_BLUE = (1, 0, 0)
SIDE_COL_BLUE = 'b'

SIDE_DIR_RIGHT = (0, 1, 0)
SIDE_DIR_LEFT = (0, -1, 0)
SIDE_DIR_BACK = (-1, 0, 0)
SIDE_DIR_FRONT = (1, 0, 0)
SIDE_DIR_UP = (0, 0, 1)
SIDE_DIR_DOWN = (0, 0, -1)

SIDE_DIRS = np.array([SIDE_DIR_RIGHT, SIDE_DIR_LEFT, SIDE_DIR_BACK, SIDE_DIR_FRONT, SIDE_DIR_UP, SIDE_DIR_DOWN])

def get_linenumber():
    cf = currentframe()
    return cf.f_back.f_lineno

def error(message, lineno, action):
    print(message, lineno, '--> action: ', action)
    if action == ERR_ACTION_EXIT:
        exit(1)

while_counter = 0

def error_endless_loop(max, lineno):
    global while_counter
    while_counter += 1
    if while_counter <= max:
        return False
    else:
        error('error: endless loop in line #', lineno, ERR_ACTION_EXIT)

if not RUN_ON_EV3:
    fig = plt.figure()

class Face:

    def __init__(self, initdir, initcol):
        self.direction = initdir
        self.color = initcol
        if not RUN_ON_EV3:
            self.poly_3d_collection = 0

    def calc_verts(self, pos):
        if self.direction[0] != 0: return [
            np.add(pos, np.dot(FACE_SIZE, (np.sign(self.direction[0]), 1, 1))),
            np.add(pos, np.dot(FACE_SIZE, (np.sign(self.direction[0]), 1, -1))),
            np.add(pos, np.dot(FACE_SIZE, (np.sign(self.direction[0]), -1, -1))),
            np.add(pos, np.dot(FACE_SIZE, (np.sign(self.direction[0]), -1, 1)))]
        if self.direction[1] != 0: return [
            np.add(pos, np.dot(FACE_SIZE, (1, np.sign(self.direction[1]), 1))),
            np.add(pos, np.dot(FACE_SIZE, (1, np.sign(self.direction[1]), -1))),
            np.add(pos, np.dot(FACE_SIZE, (-1, np.sign(self.direction[1]), -1))),
            np.add(pos, np.dot(FACE_SIZE, (-1, np.sign(self.direction[1]), 1)))]
        if self.direction[2] != 0: return [
            np.add(pos, np.dot(FACE_SIZE, (1, 1, np.sign(self.direction[2])))),
            np.add(pos, np.dot(FACE_SIZE, (1, -1, np.sign(self.direction[2])))),
            np.add(pos, np.dot(FACE_SIZE, (-1, -1, np.sign(self.direction[2])))),
            np.add(pos, np.dot(FACE_SIZE, (-1, 1, np.sign(self.direction[2]))))]

    def rotate(self, rot_mat):
        self.direction = rot_mat.dot(self.direction)


class Stone:

    def __init__(self, initpos):
        self.position = initpos
        self.faces = np.array([])
        if (np.dot(self.position, SIDE_DIR_RED) > 0):
            self.faces = np.append(self.faces, Face(SIDE_DIR_RED, SIDE_COL_RED))
        if (np.dot(self.position, SIDE_DIR_ORANGE) > 0):
            self.faces = np.append(self.faces, Face(SIDE_DIR_ORANGE, SIDE_COL_ORANGE))
        if (np.dot(self.position, SIDE_DIR_YELLOW) > 0):
            self.faces = np.append(self.faces, Face(SIDE_DIR_YELLOW, SIDE_COL_YELLOW))
        if (np.dot(self.position, SIDE_DIR_WHITE) > 0):
            self.faces = np.append(self.faces, Face(SIDE_DIR_WHITE, SIDE_COL_WHITE))
        if (np.dot(self.position, SIDE_DIR_GREEN) > 0):
            self.faces = np.append(self.faces, Face(SIDE_DIR_GREEN, SIDE_COL_GREEN))
        if (np.dot(self.position, SIDE_DIR_BLUE) > 0):
            self.faces = np.append(self.faces, Face(SIDE_DIR_BLUE, SIDE_COL_BLUE))

    def draw(self, ax):
        for f in self.faces:
            verts = [f.calc_verts(self.position)]

            if not RUN_ON_EV3:
                if f.poly_3d_collection == 0:
                    f.poly_3d_collection = Poly3DCollection(
                        verts, linewidths=1, edgecolors='k', facecolor=f.color, alpha=1)
                    ax.add_collection3d(f.poly_3d_collection)
                # ax.scatter(self.position[0], self.position[1], self.position[2])
                else:
                    f.poly_3d_collection.set_verts(verts)

    def rotate(self, rot_mat):
        self.position = rot_mat.dot(self.position)
        for f in self.faces:
            f.rotate(rot_mat)

    def get_col_of_dir(self, dir):
        for f in self.faces:
            if np.dot(f.direction, dir) == 1 :
                    return f.color

class Cube:
    # class vars
    rotx = 0
    roty = 0
    rotz = 0

    def __init__(self, ax):
        self.subplot = ax
        initStonePos = np.array([
            (-1, 1, -1), (0, 1, -1), (1, 1, -1),
            (-1, 0, -1), (1, 0, -1),
            (-1, -1, -1), (0, -1, -1), (1, -1, -1),
            (-1, 1, 0), (1, 1, 0), (1, -1, 0), (-1, -1, 0),
            (-1, 1, 1), (0, 1, 1), (1, 1, 1),
            (-1, 0, 1), (1, 0, 1),
            (-1, -1, 1), (0, -1, 1), (1, -1, 1),
            (1, 0, 0), (-1, 0, 0),
            (0, 1, 0), (0, -1, 0),
            (0, 0, 1), (0, 0, -1)
        ])

        self.rotx = np.array([
            [1, 0, 0],
            [0, 0, 1],
            [0, -1, 0]])
        self.rotx_ = np.array([
            [1, 0, 0],
            [0, 0, -1],
            [0, 1, 0]])

        self.roty = np.array([
            [0, 0, 1],
            [0, 1, 0],
            [-1, 0, 0]])
        self.roty_ = np.array([
            [0, 0, -1],
            [0, 1, 0],
            [1, 0, 0]])

        self.rotz = np.array([
            [0, 1, 0],
            [-1, 0, 0],
            [0, 0, 1]])
        self.rotz_ = np.array([
            [0, -1, 0],
            [1, 0, 0],
            [0, 0, 1]])

        self.stones = np.array([])

        for pos in initStonePos:
            self.stones = np.append(self.stones, Stone(pos))

    def get_color_of_side(self, side):
        for s in self.stones:
            if s.faces.size == 1 and np.array_equal(s.faces[0].direction, side):
                return s.faces[0].color

    def get_side_of_color(self, color):
        for s in self.stones:
            if s.faces.size == 1 and s.faces[0].color == color: return s.faces[0].direction

    def get_edge_stone(self, col1, col2):
        for s in self.stones:
            if s.faces.size == 2:
                if sorted(s.faces[0].color + s.faces[1].color) == sorted(col1 + col2):
                    return s
        error('edge stone not found. code line ', get_linenumber(), ERR_ACTION_EXIT)

    def get_corner_stone(self, col1, col2, col3):
        for s in self.stones:
            if s.faces.size == 3:
                if sorted(s.faces[0].color + s.faces[1].color + s.faces[2].color) == sorted(col1 + col2 + col3):
                    return s
        error('corner stone not found. code line ', get_linenumber(), ERR_ACTION_EXIT)

    def stones_side(self, side):
        y = np.array([])
        for s in self.stones:
            if np.dot(s.position, side) == 1: y = np.append(y, s)
        return y

    def draw(self):
        for s in self.stones:
            s.draw(self.subplot)

    # switcher functions
    def turn_R(self):
        for s in self.stones_side(SIDE_DIR_RIGHT):
                    s.rotate(self.roty_)
        mcd.turn_R()
        return

    def turn_r(self):
        for s in self.stones_side(SIDE_DIR_RIGHT):
            s.rotate(self.roty)
        mcd.turn_r()
        return

    def turn_L(self):
        for s in self.stones_side(SIDE_DIR_LEFT):
            s.rotate(self.roty)
        mcd.turn_L()
        return

    def turn_l(self):
        for s in self.stones_side(SIDE_DIR_LEFT):
            s.rotate(self.roty_)
        mcd.turn_l()
        return

    def turn_U(self):
        for s in self.stones_side(SIDE_DIR_UP):
            s.rotate(self.rotz)
        mcd.turn_U()

    def turn_u(self):
        for s in self.stones_side(SIDE_DIR_UP):
            s.rotate(self.rotz_)
        mcd.turn_u()
        return

    def turn_D(self):
        for s in self.stones_side(SIDE_DIR_DOWN):
            s.rotate(self.rotz)
        mcd.turn_D()
        return

    def turn_d(self):
        for s in self.stones_side(SIDE_DIR_DOWN):
            s.rotate(self.rotz_)
        mcd.turn_d()
        return

    def turn_F(self):
        for s in self.stones_side(SIDE_DIR_FRONT):
            s.rotate(self.rotx)
        mcd.turn_F()
        return

    def turn_f(self):
        for s in self.stones_side(SIDE_DIR_FRONT):
            s.rotate(self.rotx_)
        mcd.turn_f()
        return

    def turn_B(self):
        for s in self.stones_side(SIDE_DIR_BACK):
            s.rotate(self.rotx)
        mcd.turn_B()
        return

    def turn_b(self):
        for s in self.stones_side(SIDE_DIR_BACK):
            s.rotate(self.rotx_)
        mcd.turn_b()
        return

    def turn_C(self):
        for s in self.stones:
            s.rotate(self.rotz)
        mcd.turn_C()
        return

    def turn_c(self):
        for s in self.stones:
            s.rotate(self.rotz_)
        mcd.turn_c()
        return

    def turn_side(self, cmd):
        switcher = {
            'R': self.turn_R,
            'r': self.turn_r,
            'L': self.turn_L,
            'l': self.turn_l,
            'F': self.turn_F,
            'f': self.turn_f,
            'B': self.turn_B,
            'b': self.turn_b,
            'U': self.turn_U,
            'u': self.turn_u,
            'D': self.turn_D,
            'd': self.turn_d,
            'C': self.turn_C,
            'c': self.turn_c
        }
        for chr in cmd:
            func = switcher.get(chr, lambda: "")
            func()
            if not RUN_ON_EV3:
                self.draw()
                fig.show()
                fig.canvas.flush_events()
            t.sleep(1)

    def is_stone_pos_correct(self, s):
        col1 = ''
        col2 = ''
        for f in s.faces:
            col1 = col1 + f.color
            col2 = col2 + self.get_color_of_side(f.direction)
        if sorted(col1) == sorted(col2):
            return True
        else:
            return False

    def is_stone_correct(self, s):
        for f in s.faces:
            if self.get_color_of_side(f.direction) != f.color:
                return False
        return True

    def stone_on_side(self, s, side):
        # print(s.position, ' * ', side, ' = ', np.dot(s.position, side))
        if np.dot(s.position, side) > 0:
            return True
        else:
            return False

    def get_wrong_edge_stones(self, side):
        s_side = self.stones_side(side)
        ws = np.array([])
        for s in s_side:
            if s.faces.size == 2:
                if not self.is_stone_correct(s): ws = np.append(ws, s)
        return ws

    def get_wrong_corner_stones(self, side):
        s_side = self.stones_side(side)
        ws = np.array([])
        for s in s_side:
            if s.faces.size == 3:
                if not self.is_stone_correct(s): ws = np.append(ws, s)
        return ws

    def get_correct_stone(self, ws):
        current_face_colors = np.array([])
        target_face_colors = np.array([])
        for f in ws.faces:
            current_face_colors = np.append(current_face_colors, f.color)
            target_face_colors = np.append(target_face_colors, self.get_color_of_side(f.direction))
        #print('current face colors: ', current_face_colors)
        #print('target face colors: ', target_face_colors)

        for s in self.stones:
            if s.faces.size == target_face_colors.size:
                stone_face_colors = np.array([])
                for f in s.faces: stone_face_colors = np.append(stone_face_colors, f.color)
                #print('stone face colors : ', stone_face_colors)
                # union1d: return the unique, sorted array of values that are in either of the two input arrays
                if np.union1d(target_face_colors, stone_face_colors).size == target_face_colors.size:
                    return s

    def is_min_corner_dist(self, cs1, cs2):
        #print('corner dist: ', np.linalg.norm(cs1 - cs2))
        return np.linalg.norm(cs1 - cs2) == 2

class CubeSolver:

    def __init__(self, cube):
        self.cube = cube

    def build_down_side(self):
        global while_counter
        # build edges on white side
        wrong_edge_stones = self.cube.get_wrong_edge_stones(self.cube.get_side_of_color(SIDE_COL_WHITE))
        print('number of wrong edge stones at white side: ', wrong_edge_stones.size)
        # fill edges with stones by the correct one
        for ws in wrong_edge_stones:
            # store correct stone
            cs = self.cube.get_correct_stone(ws)
            # store position where this stone must be placed
            cp = ws.position
            # check if correct stone is not on yellow/upper side
            if not self.cube.stone_on_side(cs, self.cube.get_side_of_color(SIDE_COL_YELLOW)):
                # turn cube till correct stone is on front side
                while_counter = 0
                while not self.cube.stone_on_side(cs, SIDE_DIR_FRONT) and not error_endless_loop(4, get_linenumber()):
                    self.cube.turn_side('C')
                    cp = self.cube.rotz.dot(cp)  # if cube is turned then rotate as well target position for the correct stone !!!
                # move correct stone to yellow/upper side and front side
                if self.cube.stone_on_side(cs, SIDE_DIR_LEFT):
                    self.cube.turn_side('FUfu')
                elif self.cube.stone_on_side(cs, SIDE_DIR_RIGHT):
                    self.cube.turn_side('fUFu')
                elif self.cube.stone_on_side(cs, SIDE_DIR_DOWN):
                    self.cube.turn_side('FFUffu')
                else: error('error in solver: bottom edge stone not found in line #', get_linenumber(), ERR_ACTION_EXIT)

            # move correct stone on upper side above correct bottom position
            #print(cp, cs.position, np.dot(cp, cs.position))
            while_counter = 0
            while np.dot(cp, cs.position) != 0 and not error_endless_loop(4, get_linenumber()): #error here !!! turn of cube dis not considered in target_positions
                self.cube.turn_side('U')
                #print(cp, cs.position, np.dot(cp, cs.position))
            #print(ws.position, np.dot(ws.position, SIDE_DIR_FRONT))

            # exchange upper/front edge with lower front edge
            while_counter = 0
            while not self.cube.stone_on_side(ws, SIDE_DIR_FRONT) and not error_endless_loop(4, get_linenumber()):
                self.cube.turn_side('C')
                cp = self.cube.rotz.dot(cp)  # if cube is turned then rotate as well target position for the correct stone !!!
                #print(ws.position, np.dot(ws.position, SIDE_DIR_FRONT))
            for f in cs.faces:
                #print(f.color, SIDE_COL_WHITE)
                if f.color == SIDE_COL_WHITE:
                    #print(f.direction, SIDE_DIR_WHITE)
                    if np.dot(f.direction, SIDE_DIR_WHITE) == -1:
                        self.cube.turn_side('LrfflR')
                    else:
                        self.cube.turn_side('ULrflR')

        print('white edges as bottom side are correct')
        t.sleep(1)

        # build corners on white side
        wrong_corner_stones = self.cube.get_wrong_corner_stones(self.cube.get_side_of_color(SIDE_COL_WHITE))
        print('number of wrong corner stones at white side: ', wrong_corner_stones.size)
        for ws in wrong_corner_stones:
            cs = self.cube.get_correct_stone(ws)
            cp = ws.position
            # check if stone not already on right place due to former moves
            if not self.cube.is_stone_correct(cs):
                # ensure correct stone is on front side
                while_counter = 0
                while not self.cube.stone_on_side(cs, SIDE_DIR_FRONT) and not error_endless_loop(4, get_linenumber()):
                    self.cube.turn_side('C')
                    cp = self.cube.rotz.dot(cp)  # if cube is turned then rotate as well target position for the correct stone !!!
                print('correct corner on front-side')

                if not self.cube.stone_on_side(cs, SIDE_DIR_UP):
                    # move correct corner stone to front/upper side
                    if self.cube.stone_on_side(cs, SIDE_DIR_LEFT) and self.cube.stone_on_side(cs, SIDE_DIR_DOWN):
                        self.cube.turn_side('FUfu')
                    elif self.cube.stone_on_side(cs, SIDE_DIR_RIGHT) and self.cube.stone_on_side(cs, SIDE_DIR_DOWN):
                        self.cube.turn_side('fuFU')
                    else:
                        error('error in solver: failed to move corner stone to front/upper side in line #', get_linenumber(), ERR_ACTION_EXIT)
                    print('correct corner stone on front/upper side')
                    #print(cp, cs.position)

                while_counter = 0
                while not self.cube.is_min_corner_dist(cp, cs.position) and not error_endless_loop(4, get_linenumber()):
                    self.cube.turn_side('U')
                while_counter = 0
                while not self.cube.stone_on_side(cs, SIDE_DIR_FRONT) and not error_endless_loop(4, get_linenumber()):
                    self.cube.turn_side('C')
                    cp = self.cube.rotz.dot(cp)  # if cube is turned then rotate as well target position for the correct stone !!!
                if self.cube.stone_on_side(cs, SIDE_DIR_RIGHT):
                    # move right corner stone to white bottom side
                    if cs.get_col_of_dir(SIDE_DIR_FRONT) == SIDE_COL_WHITE :
                        self.cube.turn_side('URur')
                    elif cs.get_col_of_dir(SIDE_DIR_RIGHT) == SIDE_COL_WHITE :
                        self.cube.turn_side('RUr')
                    elif cs.get_col_of_dir(SIDE_DIR_UP) == SIDE_COL_WHITE :
                        self.cube.turn_side('RurfUUF')
                    else:
                        error('inconsistent faces of stone', get_linenumber(), ERR_ACTION_EXIT)
                else:
                    # move left corner stone to white bottom side
                    if cs.get_col_of_dir(SIDE_DIR_FRONT) == SIDE_COL_WHITE :
                        self.cube.turn_side('ulUL')
                    elif cs.get_col_of_dir(SIDE_DIR_LEFT) == SIDE_COL_WHITE :
                        self.cube.turn_side('luL')
                    elif cs.get_col_of_dir(SIDE_DIR_UP) == SIDE_COL_WHITE :
                        self.cube.turn_side('lURFuuf')
                    else:
                        error('inconsistent faces of stone', get_linenumber(), ERR_ACTION_EXIT)
                #print(cp, cs.position, np.dot(cp, cs.position))

    def build_mid_ring(self):
        mid_stones = np.array([])
        mid_stones = np.append(mid_stones,
            [self.cube.get_edge_stone(SIDE_COL_RED, SIDE_COL_GREEN),
            self.cube.get_edge_stone(SIDE_COL_RED, SIDE_COL_BLUE),
            self.cube.get_edge_stone(SIDE_COL_ORANGE, SIDE_COL_GREEN),
            self.cube.get_edge_stone(SIDE_COL_ORANGE, SIDE_COL_BLUE)])

        #for ms in mid_stones:
            #print('mid stone colors: ', ms.faces[0].color, ms.faces[1].color, 'correct? ', self.cube.is_stone_correct(ms))

        for ms in mid_stones:
            #print('mid stone colors: ', ms.faces[0].color, ms.faces[1].color, 'correct? ', self.cube.is_stone_correct(ms))
            if not self.cube.is_stone_correct(ms):
                # if mid stone not on UP side, then move to UP side
                if not self.cube.stone_on_side(ms, SIDE_DIR_UP):
                    # ensure that mid stone is on front side
                    print('move mid stone to front')
                    while not self.cube.stone_on_side(ms, SIDE_DIR_FRONT):
                        self.cube.turn_side('C')
                    # move mid stone to UP side
                    print('move mid stone to up side')
                    if self.cube.stone_on_side(ms, SIDE_DIR_RIGHT):
                        self.cube.turn_side('URurufUF')
                    elif self.cube.stone_on_side(ms, SIDE_DIR_LEFT):
                        self.cube.turn_side('ulULUFuf')
                    else:
                        error('mixed up mid stones in line ', get_linenumber(), ERR_ACTION_EXIT)
                print('move mid stone on up side to correct side with same color')
                #print('color of face0 side:', self.cube.get_color_of_side(ms.faces[0].direction), 'color of face0: ', ms.faces[0].color)
                #print('color of face1 side:', self.cube.get_color_of_side(ms.faces[1].direction), 'color of face1: ', ms.faces[1].color)
                while not ( self.cube.get_color_of_side(ms.faces[0].direction) == ms.faces[0].color or
                            self.cube.get_color_of_side(ms.faces[1].direction) == ms.faces[1].color):
                    self.cube.turn_side('U')
                    #print('color of face0 side:', self.cube.get_color_of_side(ms.faces[0].direction), 'color of face0: ', ms.faces[0].color)
                    #print('color of face1 side:', self.cube.get_color_of_side(ms.faces[1].direction), 'color of face1: ', ms.faces[1].color)
                print('turn cube till correct mid stone is at front side')
                while not self.cube.stone_on_side(ms, SIDE_DIR_FRONT):
                    self.cube.turn_side('C')
                print('insert mid stone to correct position')
                if (ms.faces[0].color == self.cube.get_color_of_side(SIDE_DIR_RIGHT) or
                    ms.faces[1].color == self.cube.get_color_of_side(SIDE_DIR_RIGHT)):
                    self.cube.turn_side('URurufUF')
                elif (ms.faces[0].color == self.cube.get_color_of_side(SIDE_DIR_LEFT) or
                      ms.faces[1].color == self.cube.get_color_of_side(SIDE_DIR_LEFT)):
                    self.cube.turn_side('ulULUFuf')
                else:
                    error('mixed up mid stones in line ', get_linenumber(), ERR_ACTION_EXIT)

    def build_top_edges(self):
        top_edges = np.array([])
        num_correct_top_edges = np.array([0,0,0,0])
        top_edges = np.append(top_edges,
                               [self.cube.get_edge_stone(SIDE_COL_YELLOW, SIDE_COL_BLUE),
                                self.cube.get_edge_stone(SIDE_COL_YELLOW, SIDE_COL_RED),
                                self.cube.get_edge_stone(SIDE_COL_YELLOW, SIDE_COL_GREEN),
                                self.cube.get_edge_stone(SIDE_COL_YELLOW, SIDE_COL_ORANGE)])
        for turn in range(4):
            num_correct_top_edges[turn] = 0
            for s in top_edges:
                if self.cube.is_stone_pos_correct(s):
                    num_correct_top_edges[turn] = num_correct_top_edges[turn] + 1
            print('after ', turn, ' turns correct edge stones: ', np.amax(num_correct_top_edges), ' number of U-turns: ',
                  np.argmax(num_correct_top_edges))
            self.cube.turn_side('U')
        print('correct edge stones: ', np.amax(num_correct_top_edges), ' number of U-turns: ', np.argmax(num_correct_top_edges))
        t.sleep(1)

        # if max correct top edges only one, then directly start edges switching and recount correct top edges
        '''
        if np.amax(num_correct_top_edges) == 1:
            error('only one top edges is correct. this case not yet considered. line: ', get_linenumber(), ERR_ACTION_EXIT)
        
        if np.amax(num_correct_top_edges) == 1:
            # switch top edges
            self.cube.turn_side('UFRUruf')
            # recount correct top edges
            for turn in range(4):
                num_correct_top_edges[turn] = 0
                for s in top_edges:
                    if self.cube.is_stone_pos_correct(s):
                        num_correct_top_edges[turn] = + 1
                self.cube.turn_side('U')
        '''

        # turn UP side to position with max correct top edges
        print('turn UP side to position with max correct top edges. turns are: ', np.argmax(num_correct_top_edges))
        for turn in range(np.argmax(num_correct_top_edges)):
            print('turn')
            self.cube.turn_side('U')

        t.sleep(1)

        if np.amax(num_correct_top_edges) == 2:
            print('two wrong top edges detected. fix them ...')
            while not (self.cube.is_stone_pos_correct(self.cube.get_edge_stone(SIDE_COL_YELLOW, self.cube.get_color_of_side(SIDE_DIR_RIGHT))) and
                not self.cube.is_stone_pos_correct(self.cube.get_edge_stone(SIDE_COL_YELLOW, self.cube.get_color_of_side(SIDE_DIR_FRONT)))) and error_endless_loop(4, get_linenumber()):
                self.cube.turn_side('C')
            self.cube.turn_side('UFRUruf')

            # again position UP side with max correct top edges
            num_correct_top_edges = [0,0,0,0]
            for turn in range(4):
                num_correct_top_edges[turn] = 0
                for s in top_edges:
                    if self.cube.is_stone_pos_correct(s):
                        num_correct_top_edges[turn] = num_correct_top_edges[turn] + 1
                print('after ', turn, ' turns correct edge stones: ', np.amax(num_correct_top_edges),
                      ' number of U-turns: ',
                      np.argmax(num_correct_top_edges))
                self.cube.turn_side('U')
            print('correct edge stones: ', np.amax(num_correct_top_edges), ' number of U-turns: ',
                  np.argmax(num_correct_top_edges))

            # turn UP side to position with max correct top edges
            print('turn UP side to position with max correct top edges. turns are: ', np.argmax(num_correct_top_edges))
            for turn in range(np.argmax(num_correct_top_edges)):
                print('turn')
                self.cube.turn_side('U')

            # check if top edges at correct position
            count_wrong_top_edges = 0
            for s in top_edges:
                if not self.cube.is_stone_pos_correct(s):
                    count_wrong_top_edges = count_wrong_top_edges + 1
            print('wrong top edges: ', count_wrong_top_edges)

            if count_wrong_top_edges > 0:
                turns = 0
                while (not (self.cube.is_stone_pos_correct(self.cube.get_edge_stone(SIDE_COL_YELLOW, self.cube.get_color_of_side(SIDE_DIR_RIGHT))) and
                    not self.cube.is_stone_pos_correct(self.cube.get_edge_stone(SIDE_COL_YELLOW, self.cube.get_color_of_side(SIDE_DIR_FRONT))))) and turns < 4:
                    self.cube.turn_side('C')
                    turns = turns + 1
                self.cube.turn_side('UFRUruf')
        elif np.amax(num_correct_top_edges) == 4:
            # fine, nothing to do
            print('all top edges correct. nothing to do.')
            pass
        else:
            error('inconsistent number of correct top edges: ', np.amax(num_correct_top_edges), ERR_ACTION_EXIT)

        ##### Problem, wenn nur die gegenueberliegenden edge stones passen
        '''
        for s in top_edges:
            if not self.cube.is_stone_correct():
                while not 
        '''

def main():
    if not RUN_ON_EV3:
        # init graphics
        #fig = plt.figure()
        ax = fig.add_subplot(111, projection='3d')
        ax.set_xlim(-2, 2)
        ax.set_ylim(-2, 2)
        ax.set_zlim(-2, 2)
        ax.azim = 10
        ax.elev = 20
        ax.plot([0, 3], [0, 0], [0, 0], '--k', color='b', linewidth=3)
        ax.plot([0, 0], [0, 3], [0, 0], '--k', color='r', linewidth=3)
        ax.plot([0, 0], [0, 0], [0, 3], '--k', color='y', linewidth=3)
        ax.azim = 10
        ax.elev = -40

    # init cube
    cube = Cube(ax)
    if not RUN_ON_EV3:
        #plt.show(block=False)
        fig.show()

    if RUN_ON_EV3:
        print('Robot Starting')
        # ev3.Sound.speak('Okay folks... Let us solve the cube!').wait()
        mcd.ev3.Sound.speak('Okay cube!').wait()
        print('Motor start turning...')

    # turn sides
    cube.turn_side('URurufUFUUulULUFuf') #wrong mid stones
    #cube.turn_side('RBLF') #completely destroyed
    #cube.turn_side('UFRUrufUUUFRUruf')
    #cube.turn_side('U')

    if not RUN_ON_EV3:
        fig.show()
        fig.canvas.flush_events()

    t.sleep(1)

    cube_solver = CubeSolver(cube)
    cube_solver.build_down_side()
    cube_solver.build_mid_ring()
    cube_solver.build_top_edges()

    if not RUN_ON_EV3:
        fig.show()
        fig.canvas.flush_events()

    print('end')

    while 1:
        t.sleep(0.5)
        cube.turn_side('C')
    #t.sleep(5)

    if RUN_ON_EV3:
        motor_a.stop(stop_action="coast")
        motor_b.stop(stop_action="coast")
        #ev3.Sound.speak('Cube is solved!').wait()


if __name__ == "__main__":
    main()
