# install packages on ev3:
# $ sudo apt-get update
# $ sudo apt install python3-sympy python3-msvcrt
# $ sudo apt-get install python3-pip
# $ sudo pip3 install sympy
from magiccube_main import RUN_ON_EV3
#import msvcrt as ms
import numpy as np
import sympy as sp
PI = sp.pi

if not RUN_ON_EV3:
    import matplotlib
    matplotlib.use('TkAgg')
    import matplotlib.pyplot as plt
    from mpl_toolkits.mplot3d import Axes3D
    from mpl_toolkits.mplot3d.art3d import Poly3DCollection, Line3DCollection
    GFX_WAIT_SECS = 0.0

from time import sleep
from inspect import currentframe
import magiccube_device as mcd

# sympy provides a symbolic solver, but...
# numpy doesn't know how to handle sympy's Float type ==> thus, convert it to a numpy array
# https://stackoverflow.com/questions/51617211/numpy-standard-deviation-attributeerror-float-object-has-no-attribute-sqrt
def scos(x): return np.array(sp.N(sp.cos(x)), dtype=np.float)
def ssin(x): return np.array(sp.N(sp.sin(x)), dtype=np.float)

#def wait(): return ms.getch()
def wait(): sleep(GFX_WAIT_SECS)
#def wait():
#    while (not matplotlib.pyplot.waitforbuttonpress()): pass

global GlobalColorCounter   # debug OKO


ERR_ACTION_EXIT = 1
FACE_SIZE       = 0.4
SIDE_DIR_RED    = np.array([0, 1, 0])
SIDE_COL_RED    = 'r'
SIDE_DIR_ORANGE = np.array([0, -1, 0])
SIDE_COL_ORANGE = 'c' # [1.0, 0.4, 0.0]
SIDE_DIR_YELLOW = np.array([0, 0, 1])
SIDE_COL_YELLOW = 'y'
SIDE_DIR_WHITE  = np.array([0, 0, -1])
SIDE_COL_WHITE  = 'w'
SIDE_DIR_GREEN  = np.array([-1, 0, 0])
SIDE_COL_GREEN  = 'g'
SIDE_DIR_BLUE   = np.array([1, 0, 0])
SIDE_COL_BLUE   = 'b'
SIDE_DIR_RIGHT  = np.array([0, 1, 0])
SIDE_DIR_LEFT   = np.array([0, -1, 0])
SIDE_DIR_BACK   = np.array([-1, 0, 0])
SIDE_DIR_FRONT  = np.array([1, 0, 0])
SIDE_DIR_UP     = np.array([0, 0, 1])
SIDE_DIR_DOWN   = np.array([0, 0, -1])
SIDE_DIRS = np.array([SIDE_DIR_RIGHT, SIDE_DIR_LEFT, SIDE_DIR_BACK, SIDE_DIR_FRONT, SIDE_DIR_UP, SIDE_DIR_DOWN])

def get_linenumber():
    cf = currentframe()
    return cf.f_back.f_lineno

def msg(message, lineno):
    print(lineno, ': ', message)

def error(message, lineno, action):
    msg(message + ' --> action: ' + str(action), lineno)
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

    def __init__(self, pos):
        self.position = pos
        self.faces = np.array([])
        return

    def init_default_faces(self):
        # expect only stone position and add generate correct faces
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
        return

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
            if np.allclose(np.dot(f.direction, dir), 1):
                    return f.color

class Cube:

    def __init__(self, ax):
        self.subplot = ax
        initStonePos = np.array([
            (-1., 1., -1.), (0., 1., -1.), (1., 1., -1.),
            (-1., 0., -1.), (1., 0., -1.),
            (-1., -1., -1.), (0., -1., -1.), (1., -1., -1.),
            (-1., 1., 0.), (1., 1., 0.), (1., -1., 0.), (-1., -1., 0.),
            (-1., 1., 1.), (0., 1., 1.), (1., 1., 1.),
            (-1., 0., 1.), (1., 0., 1.),
            (-1., -1., 1.), (0., -1., 1.), (1., -1., 1.),
            (1., 0., 0.), (-1., 0., 0.),
            (0., 1., 0.), (0., -1., 0.),
            (0., 0., 1.), (0., 0., -1.)
        ])

        self.stones = np.array([])

        for pos in initStonePos:
            self.stones = np.append(self.stones, Stone(pos))
        return

    def rotx(self, rounds = 0.25):
        s = ssin(2. * PI * rounds)
        c = scos(2. * PI * rounds)
        return np.array([
            [ 1.0, 0.0, 0.0],
            [ 0.0,   c,  -s],
            [ 0.0,   s,   c]])

    def rotx_(self, rounds = -0.25):
        return self.rotx(rounds=rounds)

    def roty(self, rounds = 0.25):
        s = ssin(2. * PI * rounds)
        c = scos(2. * PI * rounds)
        return np.array([
            [   c,  0.0,  s],
            [   0.0,  1.0,  0.0],
            [  -s,  0.0,  c]])

    def roty_(self, rounds = -0.25):
        return self.roty(rounds=rounds)

    def rotz(self, rounds = 0.25):
        s = ssin(2. * PI * rounds)
        c = scos(2. * PI * rounds)
        return np.array([
            [   c, -s,  0.0],
            [   s,  c,  0.0],
            [   0.0,  0.0,  1.0]])

    def rotz_(self, rounds = -0.25):
        return self.rotz(rounds = rounds)

    class MoveUpAllCubeSides:
        def __init__(self, parent):
            self.parent = parent
            return

        def __iter__(self):
            self.a = 1
            return self

        def __next__(self):
            x = self.a
            if 2 <= x <= 4:
                self.parent.turn_side('T')
            elif x == 5:
                self.parent.turn_side('Y')
                self.parent.turn_side('T')
            elif x == 6:
                self.parent.turn_side('TT')
            elif x > 6:
                self.parent.turn_side('yTy')
                raise StopIteration
            self.a += 1
            return x

    def create_MoveUpAllCubeSides(self):
        return Cube.MoveUpAllCubeSides(self)

    def init_solved_cube(self):
        for s in self.stones:
            s.init_default_faces()
        return

    def init_physical_cube(self):
        # read colors of physical cube and store at digital twin
        dirs =  {0: [SIDE_DIR_UP],
                 1: [SIDE_DIR_UP, SIDE_DIR_BACK],
                 2: [SIDE_DIR_UP, SIDE_DIR_BACK, SIDE_DIR_LEFT],
                 3: [SIDE_DIR_UP, SIDE_DIR_LEFT],
                 4: [SIDE_DIR_UP, SIDE_DIR_FRONT, SIDE_DIR_LEFT],
                 5: [SIDE_DIR_UP, SIDE_DIR_FRONT],
                 6: [SIDE_DIR_UP, SIDE_DIR_FRONT, SIDE_DIR_RIGHT],
                 7: [SIDE_DIR_UP, SIDE_DIR_RIGHT],
                 8: [SIDE_DIR_UP, SIDE_DIR_BACK, SIDE_DIR_RIGHT]}

        move_up_all_cube_sides = self.create_MoveUpAllCubeSides()
        it_move_up_sides = iter(move_up_all_cube_sides)
        global i
        for i in it_move_up_sides:
            # measure all nine stone colors of upside
            cols = self.measure_upside_stone_colors()
            # store stone colors of upside
            for n in dirs:
                self.add_face_to_stone(self.get_stone_by_face_dirs(dirs[n]), Face(SIDE_DIR_UP, cols[n]))
        return

    def add_face_to_stone(self, s, f):
        s.faces = np.append(s.faces, f)
        return

    def get_stone_by_face_dirs(self, dirs):
        for s in self.stones:
            sum = 0
            for d in dirs:
                if self.stone_on_side(s, d):
                    sum = sum + 1
            sum_all = 0
            for d_all in SIDE_DIRS:
                if self.stone_on_side(s, d_all):
                    sum_all = sum_all + 1
            if sum == sum_all == len(dirs):
                return s
        error('stone not found by face directions', get_linenumber(), ERR_ACTION_EXIT)
        return

    def measure_upside_stone_colors(self):
        cols = ['', '', '', '', '', '', '', '', '']
        cube_turn_cmd = ['', '', 'Y', 'Y', 'Y', 'Y', 'Y', 'Y', 'Y']
        mot_col_pos = [mcd.MOT_COL_POS_CENTER,
                       mcd.MOT_COL_POS_EDGE, mcd.MOT_COL_POS_CORNER,
                       mcd.MOT_COL_POS_EDGE, mcd.MOT_COL_POS_CORNER,
                       mcd.MOT_COL_POS_EDGE, mcd.MOT_COL_POS_CORNER,
                       mcd.MOT_COL_POS_EDGE, mcd.MOT_COL_POS_CORNER]
        for (col_index, cmd, pos) in zip(range(9), cube_turn_cmd, mot_col_pos):
            if cmd == 'Y':
                self.turn_Y(rounds=0.125)
            mcd.move_color_sensor_to_pos(pos)
            cols[col_index] = mcd.read_color(i-1) #debug OKO)
        # 8 x 0.125 = one full turnaround
        self.turn_Y(rounds=0.125)
        return cols

    def get_color_of_side(self, side):
        for s in self.stones:
            if s.faces.size == 1 and np.allclose(s.faces[0].direction, side):
                return s.faces[0].color
        error('could not find color of side, since center stone is missing for direction: ' + str(side), get_linenumber(), ERR_ACTION_EXIT)

    def get_side_of_color(self, color):
        for s in self.stones:
            if s.faces.size == 1 and s.faces[0].color == color: return s.faces[0].direction
        error('could not find side of color, since center stone is missing for color: ' + color,
              get_linenumber(), ERR_ACTION_EXIT)

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
            if np.allclose(np.dot(s.position, side), 1): y = np.append(y, s)
        return y

    def draw(self):
        for s in self.stones:
            s.draw(self.subplot)

    # switcher functions
    def turn_R(self, rounds=-0.25):
        for s in self.stones_side(SIDE_DIR_RIGHT):
            s.rotate(self.roty_(rounds=rounds))
        mcd.turn_R(rounds=rounds)
        return

    def turn_r(self, rounds=0.25):
        for s in self.stones_side(SIDE_DIR_RIGHT):
            s.rotate(self.roty(rounds=rounds))
        mcd.turn_r(rounds=rounds)
        return

    def turn_L(self, rounds=0.25):
        for s in self.stones_side(SIDE_DIR_LEFT):
            s.rotate(self.roty(rounds=rounds))
        mcd.turn_L(rounds=rounds)
        return

    def turn_l(self, rounds=-0.25):
        for s in self.stones_side(SIDE_DIR_LEFT):
            s.rotate(self.roty_(rounds=rounds))
        mcd.turn_l(rounds=rounds)
        return

    def turn_U(self, rounds=-0.25):
        for s in self.stones_side(SIDE_DIR_UP):
            s.rotate(self.rotz(rounds=rounds))
        mcd.turn_U(rounds=rounds)
        return

    def turn_u(self, rounds=0.25):
        for s in self.stones_side(SIDE_DIR_UP):
            s.rotate(self.rotz_(rounds=rounds))
        mcd.turn_u(rounds=rounds)
        return

    def turn_D(self, rounds=0.25):
        for s in self.stones_side(SIDE_DIR_DOWN):
            s.rotate(self.rotz_(rounds=rounds))
        mcd.turn_D(rounds=rounds)
        return

    def turn_d(self, rounds=-0.25):
        for s in self.stones_side(SIDE_DIR_DOWN):
            s.rotate(self.rotz(rounds=rounds))
        mcd.turn_d(rounds=rounds)
        return

    def turn_F(self, rounds=-0.25):
        for s in self.stones_side(SIDE_DIR_FRONT):
            s.rotate(self.rotx(rounds=rounds))
        mcd.turn_F(rounds=rounds)
        return

    def turn_f(self, rounds=0.25):
        for s in self.stones_side(SIDE_DIR_FRONT):
            s.rotate(self.rotx_(rounds=rounds))
        mcd.turn_f(rounds=rounds)
        return

    def turn_B(self, rounds=0.25):
        for s in self.stones_side(SIDE_DIR_BACK):
            s.rotate(self.rotx(rounds=rounds))
        mcd.turn_B(rounds=rounds)
        return

    def turn_b(self, rounds=-0.25):
        for s in self.stones_side(SIDE_DIR_BACK):
            s.rotate(self.rotx_(rounds=rounds))
        mcd.turn_b(rounds=rounds)
        return

    def turn_Y(self, rounds=0.25):
        for s in self.stones:
            s.rotate(self.rotz(rounds=rounds))
        mcd.turn_Y(rounds=rounds)
        return

    def turn_y(self, rounds=-0.25):
        for s in self.stones:
            s.rotate(self.rotz_(rounds=rounds))
        mcd.turn_y(rounds=rounds)
        return

    def turn_T(self):   # tilt move must always be a quater, since device can only flip
        for s in self.stones:
            s.rotate(self.roty())
        mcd.turn_T()
        return

    def turn_t(self):   # tilt move must always be a quater, since device can only flip
        for s in self.stones:
            s.rotate(self.roty_())
        mcd.turn_t()
        return

    def turn_side(self, cmd):
        for chr in cmd:
            # Get the method from 'self'. Default to a lambda.
            turn_method = getattr(self, 'turn_' + chr, lambda: error('turn command does not exist', get_linenumber(), ERR_ACTION_EXIT))
            turn_method()
            if not RUN_ON_EV3:
                self.draw()
                fig.show()
                fig.canvas.flush_events()
                wait()
        return

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
        for s in self.stones:
            if s.faces.size == target_face_colors.size:
                stone_face_colors = np.array([])
                for f in s.faces: stone_face_colors = np.append(stone_face_colors, f.color)
                #print('stone face colors : ', stone_face_colors)
                # union1d: return the unique, sorted array of values that are in either of the two input arrays
                if np.union1d(target_face_colors, stone_face_colors).size == target_face_colors.size:
                    return s
        error('correct stone not found', get_linenumber(), ERR_ACTION_EXIT)

    def is_min_corner_dist(self, cs1, cs2):
        return np.allclose(np.linalg.norm(cs1 - cs2), 2)

class CubeSolver:

    def __init__(self, cube):
        self.cube = cube

    def check_down_side(self):
        for s in self.cube.stones:
            if self.cube.stone_on_side(s, SIDE_DIR_DOWN) and not self.cube.is_stone_correct(s):
                return False
        return True

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
                    self.cube.turn_side('Y')
                    cp = self.cube.rotz().dot(cp)  # if cube is turned then rotate as well target position for the correct stone !!!
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
            while not np.allclose(np.dot(cp, cs.position), 0) and not error_endless_loop(4, get_linenumber()): #error here !!! turn of cube is not considered in target_positions
                self.cube.turn_side('U')
                #print(cp, cs.position, np.dot(cp, cs.position))
            #print(ws.position, np.dot(ws.position, SIDE_DIR_FRONT))

            # exchange upper/front edge with lower front edge
            while_counter = 0
            while not self.cube.stone_on_side(ws, SIDE_DIR_FRONT) and not error_endless_loop(4, get_linenumber()):
                self.cube.turn_side('Y')
                cp = self.cube.rotz().dot(cp)  # if cube is turned then rotate as well target position for the correct stone !!!
                #print(ws.position, np.dot(ws.position, SIDE_DIR_FRONT))
            for f in cs.faces:
                #print(f.color, SIDE_COL_WHITE)
                if f.color == SIDE_COL_WHITE:
                    #print(f.direction, SIDE_DIR_WHITE)
                    if np.allclose(np.dot(f.direction, SIDE_DIR_WHITE), -1):
                        self.cube.turn_side('LrfflR')
                    else:
                        self.cube.turn_side('ULrflR')
        print('white edges as bottom side are correct')

        # build corners on white side
        wrong_corner_stones = self.cube.get_wrong_corner_stones(self.cube.get_side_of_color(SIDE_COL_WHITE))
        print('number of wrong corner stones at white side: ', wrong_corner_stones.size)

        print('wrong white corner stones:')

        corner_to_pos = {}
        for ws in wrong_corner_stones:
            cs = self.cube.get_correct_stone(ws)
            corner_to_pos[cs] = ws.position

        for cs in corner_to_pos:
            print('move corner: ', cs.faces[0].color, cs.faces[1].color, cs.faces[2].color, ' from ', cs.position, ' to ',
                  corner_to_pos[cs])

            # check if stone not already on right place due to former moves
            if not self.cube.is_stone_correct(cs):
                # ensure correct stone is on front side
                while_counter = 0
                while not self.cube.stone_on_side(cs, SIDE_DIR_FRONT) and not error_endless_loop(4, get_linenumber()):
                    self.cube.turn_side('Y')
                    for s in corner_to_pos: corner_to_pos[s] = self.cube.rotz().dot(corner_to_pos[s])  # if cube is turned then rotate as well target position for the correct stone !!!
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


                while_counter = 0
                while not self.cube.is_min_corner_dist(corner_to_pos[cs], cs.position) and not error_endless_loop(4, get_linenumber()):
                    self.cube.turn_side('U')
                while_counter = 0
                while not self.cube.stone_on_side(cs, SIDE_DIR_FRONT) and not error_endless_loop(4, get_linenumber()):
                    self.cube.turn_side('Y')
                    for s in corner_to_pos: corner_to_pos[s] = self.cube.rotz().dot(corner_to_pos[s])  # if cube is turned then rotate as well target position for the correct stone !!!
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
                        self.cube.turn_side('lULFuuf')
                    else:
                        error('inconsistent faces of stone', get_linenumber(), ERR_ACTION_EXIT)

                #print(cp, cs.position, np.dot(cp, cs.position))
                #print('move ', cs.faces[0].color, cs.faces[1].color, cs.faces[2].color, ' now at pos ', cs.position,
                #      ' planned pos was ', cp, ' therefore stone is: ', self.cube.is_stone_correct(cs))

        if not self.check_down_side():
            error('Error building down side', get_linenumber(), ERR_ACTION_EXIT)
        return

    def check_mid_ring(self):
        mid_stones = np.array([])
        mid_stones = np.append(mid_stones,
                               [self.cube.get_edge_stone(SIDE_COL_RED, SIDE_COL_GREEN),
                                self.cube.get_edge_stone(SIDE_COL_RED, SIDE_COL_BLUE),
                                self.cube.get_edge_stone(SIDE_COL_ORANGE, SIDE_COL_GREEN),
                                self.cube.get_edge_stone(SIDE_COL_ORANGE, SIDE_COL_BLUE)])
        for s in mid_stones:
            if not self.cube.is_stone_correct(s):
                return False
        return True


    def build_mid_ring(self):
        mid_stones = np.array([])
        mid_stones = np.append(mid_stones,
            [self.cube.get_edge_stone(SIDE_COL_RED, SIDE_COL_GREEN),
            self.cube.get_edge_stone(SIDE_COL_RED, SIDE_COL_BLUE),
            self.cube.get_edge_stone(SIDE_COL_ORANGE, SIDE_COL_GREEN),
            self.cube.get_edge_stone(SIDE_COL_ORANGE, SIDE_COL_BLUE)])

        for ms in mid_stones:
            print('mid stone colors: ', ms.faces[0].color, ms.faces[1].color, 'correct? ', self.cube.is_stone_correct(ms))
            if not self.cube.is_stone_correct(ms):
                # if mid stone not on UP side, then move to UP side
                if not self.cube.stone_on_side(ms, SIDE_DIR_UP):
                    # ensure that mid stone is on front side
                    print('move mid stone to front')
                    while not self.cube.stone_on_side(ms, SIDE_DIR_FRONT):
                        self.cube.turn_side('Y')
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
                    self.cube.turn_side('Y')
                print('insert mid stone to correct position')
                if (ms.faces[0].color == self.cube.get_color_of_side(SIDE_DIR_RIGHT) or
                    ms.faces[1].color == self.cube.get_color_of_side(SIDE_DIR_RIGHT)):
                    self.cube.turn_side('URurufUF')
                elif (ms.faces[0].color == self.cube.get_color_of_side(SIDE_DIR_LEFT) or
                      ms.faces[1].color == self.cube.get_color_of_side(SIDE_DIR_LEFT)):
                    self.cube.turn_side('ulULUFuf')
                else:
                    error('mixed up mid stones in line ', get_linenumber(), ERR_ACTION_EXIT)

        if not self.check_mid_ring():
            error('Error building mid ring', get_linenumber(), ERR_ACTION_EXIT)
        return

    def check_top_edges(self):
        top_edges = np.array([])
        top_edges = np.append(top_edges,
                               [self.cube.get_edge_stone(SIDE_COL_YELLOW, SIDE_COL_BLUE),
                                self.cube.get_edge_stone(SIDE_COL_YELLOW, SIDE_COL_RED),
                                self.cube.get_edge_stone(SIDE_COL_YELLOW, SIDE_COL_GREEN),
                                self.cube.get_edge_stone(SIDE_COL_YELLOW, SIDE_COL_ORANGE)])
        for s in top_edges:
            if not self.cube.is_stone_correct(s):
                return False
        return True


    def build_top_edges(self):
        top_edges = np.array([])
        num_correct_top_edges = np.array([0,0,0,0])
        top_edges = np.append(top_edges,
                               [self.cube.get_edge_stone(SIDE_COL_YELLOW, SIDE_COL_BLUE),
                                self.cube.get_edge_stone(SIDE_COL_YELLOW, SIDE_COL_RED),
                                self.cube.get_edge_stone(SIDE_COL_YELLOW, SIDE_COL_GREEN),
                                self.cube.get_edge_stone(SIDE_COL_YELLOW, SIDE_COL_ORANGE)])
        for turn in range(4):
            msg('turn:' + str(turn), get_linenumber())
            num_correct_top_edges[turn] = 0
            for s in top_edges:
                if self.cube.is_stone_pos_correct(s):
                    num_correct_top_edges[turn] = num_correct_top_edges[turn] + 1
            print('after ', turn, ' turns correct edge stones: ', np.amax(num_correct_top_edges), ' number of U-turns: ',
                  np.argmax(num_correct_top_edges))
            self.cube.turn_side('U')
        print('correct edge stones: ', np.amax(num_correct_top_edges), ' number of U-turns: ', np.argmax(num_correct_top_edges))

        # turn UP side to position with max correct top edges
        print('turn UP side to position with max correct top edges. turns are: ', np.argmax(num_correct_top_edges))
        for turn in range(np.argmax(num_correct_top_edges)):
            print('turn')
            self.cube.turn_side('U')

        if np.amax(num_correct_top_edges) == 2:
            print('two wrong top edges detected. fix them ...')
            while not (self.cube.is_stone_pos_correct(self.cube.get_edge_stone(SIDE_COL_YELLOW, self.cube.get_color_of_side(SIDE_DIR_RIGHT))) and
                not self.cube.is_stone_pos_correct(self.cube.get_edge_stone(SIDE_COL_YELLOW, self.cube.get_color_of_side(SIDE_DIR_FRONT)))) and error_endless_loop(4, get_linenumber()):
                self.cube.turn_side('Y')
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
                    self.cube.turn_side('Y')
                    turns = turns + 1
                self.cube.turn_side('UFRUruf')
        elif np.amax(num_correct_top_edges) == 4:
            # fine, nothing to do
            print('all top edges correct. nothing to do.')
            pass
        else:
            error('inconsistent number of correct top edges: ', np.amax(num_correct_top_edges), ERR_ACTION_EXIT)

        print('check top edge orientation...')
        top_edges_to_flip = np.array([])
        for s in top_edges:
            if not self.cube.is_stone_correct(s):
                top_edges_to_flip = np.append(top_edges_to_flip, s)
        for s in top_edges_to_flip:
            print('wrong top edge orientation found')
            # turn up side till top edge to flip is on right side
            print('turn up side till top edge to flip is on right side')
            while not self.cube.stone_on_side(s, SIDE_DIR_RIGHT):
                self.cube.turn_side('U')
            print('flip the top edge on the right side...')
            self.cube.turn_side('RdUyRdUyRdUyRdUy')
        # turn up side till top_edges are at their place
        print('turn up side till top_edges are at their place...')
        while not self.cube.is_stone_correct(top_edges[0]):
            self.cube.turn_side('U')

        if not self.check_top_edges():
            error('Error building top edges', get_linenumber(), ERR_ACTION_EXIT)
        return

    def check_top_corners(self):
        top_corners = np.array([])
        top_corners = np.append(top_corners,
                                [self.cube.get_corner_stone(SIDE_COL_YELLOW, SIDE_COL_BLUE, SIDE_COL_RED),
                                 self.cube.get_corner_stone(SIDE_COL_YELLOW, SIDE_COL_BLUE, SIDE_COL_ORANGE),
                                 self.cube.get_corner_stone(SIDE_COL_YELLOW, SIDE_COL_RED, SIDE_COL_GREEN),
                                 self.cube.get_corner_stone(SIDE_COL_YELLOW, SIDE_COL_ORANGE, SIDE_COL_GREEN)])
        for s in top_corners:
            if not self.cube.is_stone_correct(s):
                return False
        return True

    def build_top_corners(self):
        top_corners = np.array([])
        top_corners = np.append(top_corners,
                              [self.cube.get_corner_stone(SIDE_COL_YELLOW, SIDE_COL_BLUE,   SIDE_COL_RED),
                               self.cube.get_corner_stone(SIDE_COL_YELLOW, SIDE_COL_BLUE,   SIDE_COL_ORANGE),
                               self.cube.get_corner_stone(SIDE_COL_YELLOW, SIDE_COL_RED,    SIDE_COL_GREEN),
                               self.cube.get_corner_stone(SIDE_COL_YELLOW, SIDE_COL_ORANGE, SIDE_COL_GREEN)])

        # count top corners at correct position
        top_corners_on_correct_pos = np.array([])
        for s in top_corners:
            if self.cube.is_stone_pos_correct(s):
                top_corners_on_correct_pos = np.append(top_corners_on_correct_pos, s)
        print('number of top corners at correct position: ', top_corners_on_correct_pos.size)

        if top_corners_on_correct_pos.size == 0:
            # just change some random top corners
            print('just change some random top corners...')
            self.cube.turn_side('RDRRDDRRdr')
            self.cube.turn_side('U')
            self.cube.turn_side('RDRRDDRRdr')
            self.cube.turn_side('u')
            # recount top corners at wrong position
            top_corners_on_correct_pos = np.array([])
            for s in top_corners:
                if self.cube.is_stone_pos_correct(s):
                    top_corners_on_correct_pos = np.append(top_corners_on_correct_pos, s)
            print('now number of top corners at correct position: ', top_corners_on_correct_pos.size)

        if top_corners_on_correct_pos.size == 1:
            while not (self.cube.stone_on_side(top_corners_on_correct_pos[0], SIDE_DIR_FRONT) and self.cube.stone_on_side(top_corners_on_correct_pos[0], SIDE_DIR_LEFT)):
                self.cube.turn_side('Y')
            s1_UFR = self.cube.get_corner_stone(self.cube.get_color_of_side(SIDE_DIR_UP), self.cube.get_color_of_side(SIDE_DIR_FRONT), self.cube.get_color_of_side(SIDE_DIR_RIGHT))
            s2_UBR = self.cube.get_corner_stone(self.cube.get_color_of_side(SIDE_DIR_UP), self.cube.get_color_of_side(SIDE_DIR_BACK), self.cube.get_color_of_side(SIDE_DIR_RIGHT))
            #s3_UBL = self.cube.get_corner_stone(self.cube.get_color_of_side(SIDE_DIR_UP), self.cube.get_color_of_side(SIDE_DIR_BACK), self.cube.get_color_of_side(SIDE_DIR_LEFT))

            if s2_UBR == self.cube.get_correct_stone(s1_UFR):
                self.cube.turn_side('RDRRDDRRdr')
                self.cube.turn_side('U')
                self.cube.turn_side('RDRRDDRRdr')
                self.cube.turn_side('u')
            else:
                self.cube.turn_side('U')
                self.cube.turn_side('RDRRDDRRdr')
                self.cube.turn_side('u')
                self.cube.turn_side('RDRRDDRRdr')
        elif top_corners_on_correct_pos.size == 4:
            pass
        else:
            error('inconsistent position of top corners. Check line ', get_linenumber(), ERR_ACTION_EXIT)

        # correct orientation of top corners
        runs = 0
        turns = 0
        for s in top_corners:
            while not self.cube.is_stone_correct(s):
                while not (self.cube.stone_on_side(s, SIDE_DIR_FRONT) and self.cube.stone_on_side(s, SIDE_DIR_RIGHT)):
                    if runs == 0:
                        self.cube.turn_side('Y')
                    else:
                        turns = turns + 1
                        self.cube.turn_side('U')
                print('flip top corner...')
                runs = runs + 1
                self.cube.turn_side('RfrFRfrF')

                if runs == 3:
                    print('unwind top side!')
                    for i in range(turns):
                        self.cube.turn_side('u')
                    runs = 0
                    turns = 0

        if not self.check_top_corners():
            error('Error building top corners', get_linenumber(), ERR_ACTION_EXIT)
        return

def main():
    ax=0
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
    #cube.init_solved_cube()
    cube.init_physical_cube()

    if not RUN_ON_EV3:
        #plt.show(block=False)
        fig.show()

    if RUN_ON_EV3:
        print('Robot Starting')
        # ev3.Sound.speak('Okay folks... Let us solve the cube!').wait()
        mcd.ev3.Sound.speak('Okay cube!').wait()
        print('Motor start turning...')

    # turn sides
    #cube.turn_side('URurufUFUUulULUFuf') #wrong mid stones --> solved !!
    cube.turn_side('RBLF') #completely destroyed --> solved !!
    #cube.turn_side('RBLFURBLF')  # completely destroyed --> solved !!
    #cube.turn_side('UFRUrufUUUFRUruf')
    #cube.turn_side('U')
    #mcd.turn_test()

    if not RUN_ON_EV3:
        fig.show()
        fig.canvas.flush_events()

    cube_solver = CubeSolver(cube)
    cube_solver.build_down_side()
    msg('build_down_side() finished', get_linenumber())
    cube_solver.build_mid_ring()
    msg('build_mid_ring() finished', get_linenumber())
    cube_solver.build_top_edges()
    msg('build_top_edges() finished', get_linenumber())
    cube_solver.build_top_corners()
    msg('build_top_corners() finished', get_linenumber())

    if not RUN_ON_EV3:
        fig.show()
        fig.canvas.flush_events()

    print('end')



    while 1:
        cube.turn_side('Y')
        sleep(0.5)
        #cube.turn_side('UuDdRrLlBbFfYyTt')


if __name__ == "__main__":
    main()