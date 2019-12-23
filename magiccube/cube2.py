import numpy as np
import matplotlib.pyplot as plt
import math as m
from mpl_toolkits.mplot3d import Axes3D
from mpl_toolkits.mplot3d.art3d import Poly3DCollection, Line3DCollection

FACE_SIZE = 0.4

SIDE_DIR_RED = (0, 1, 0)
SIDE_COL_RED = 'r'
SIDE_DIR_ORANGE = (0, -1, 0)
SIDE_COL_ORANGE = 'c'
SIDE_DIR_YELLOW = (0, 0, 1)
SIDE_COL_YELLOW = 'y'
SIDE_DIR_WHITE = (0, 0, -1)
SIDE_COL_WHITE = 'w'
SIDE_DIR_GREEN = (-1, 0, 0)
SIDE_COL_GREEN = 'g'
SIDE_DIR_BLUE = (1, 0, 0)
SIDE_COL_BLUE = 'b'


class Face:

    def __init__(self, initdir, initcol):
        self.direction = initdir
        self.color = initcol
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

            if f.poly_3d_collection == 0:
                f.poly_3d_collection = Poly3DCollection(
                    verts, linewidths=1, edgecolors='k', facecolor=f.color, alpha=0.8)
                ax.add_collection3d(f.poly_3d_collection)
            # ax.scatter(self.position[0], self.position[1], self.position[2])
            else:
                f.poly_3d_collection.set_verts(verts)

    def rotate(self, rot_mat):
        self.position = rot_mat.dot(self.position)
        for f in self.faces:
            f.rotate(rot_mat)


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
            (-1, -1, 1), (0, -1, 1), (1, -1, 1)
        ])

        self.rotx = np.array([
            [1, 0, 0],
            [0, 0, 1],
            [0, -1, 0]])

        self.roty = np.array([
            [0, 0, -1],
            [0, 1, 0],
            [1, 0, 0]])

        self.rotz = np.array([
            [0, 1, 0],
            [-1, 0, 0],
            [0, 0, 1]])

        self.stones = np.array([])
        # print('init')
        for pos in initStonePos:
            self.stones = np.append(self.stones, Stone(pos))
        # print(stones[-1].position)
        # self.stones_right = self.stones_left = self.stones_up = self.stones_down = self.stones_back = self.stones_front = np.array([])
        '''for s in self.stones :
            if s.position[0] > 0 : self.stones_front 	= np.append(self.stones_front, s)
            if s.position[0] < 0 : self.stones_back 	= np.append(self.stones_back, s)
            if s.position[1] > 0 : self.stones_right 	= np.append(self.stones_right, s)
            if s.position[1] < 0 : self.stones_left 	= np.append(self.stones_left, s)
            if s.position[2] > 0 : self.stones_up 		= np.append(self.stones_up, s)
            if s.position[2] < 0 : self.stones_down 	= np.append(self.stones_down, s)
        '''

    def stones_front(self):
        y = np.array([])
        for s in self.stones:
            if s.position[0] > 0: y = np.append(y, s)
        return y

    def stones_back(self):
        y = np.array([])
        for s in self.stones:
            if s.position[0] < 0: y = np.append(y, s)
        return y

    def stones_right(self):
        y = np.array([])
        for s in self.stones:
            if s.position[1] > 0: y = np.append(y, s)
        return y

    def stones_left(self):
        y = np.array([])
        for s in self.stones:
            if s.position[1] < 0: y = np.append(y, s)
        return y

    def stones_up(self):
        y = np.array([])
        for s in self.stones:
            if s.position[2] > 0: y = np.append(y, s)
        return y

    def stones_down(self):
        y = np.array([])
        for s in self.stones:
            if s.position[2] < 0: y = np.append(y, s)
        return y

    def draw(self):
        for s in self.stones:
            s.draw(self.subplot)

    def turn_side(self, turn_dir):
        # 'R' turn right side clockwise
        # 'L' turn left side clockwise
        # 'F' turn front side clockwise
        # 'B' turn back side clockwise
        # 'U' turn up side clockwise
        # 'D' turn down clockwise
        # lower case letter mean counter clockwise turn
        for chr in turn_dir:
            if chr == 'R':
                for s in self.stones_right():
                    s.rotate(self.roty)
            elif chr == 'r':
                for s in self.stones_right():
                    s.rotate(-self.roty)
            elif chr == 'L':
                for s in self.stones_left():
                    s.rotate(self.roty)
            elif chr == 'l':
                for s in self.stones_left():
                    s.rotate(-self.roty)
            elif chr == 'U':
                for s in self.stones_up():
                    s.rotate(self.rotz)
            elif chr == 'u':
                for s in self.stones_up():
                    s.rotate(-self.rotz)
            elif chr == 'D':
                for s in self.stones_down():
                    s.rotate(self.rotz)
            elif chr == 'd':
                for s in self.stones_down():
                    s.rotate(-self.rotz)
            elif chr == 'F':
                for s in self.stones_front():
                    s.rotate(self.rotx)
            elif chr == 'f':
                for s in self.stones_front():
                    s.rotate(-self.rotx)
            elif chr == 'B':
                for s in self.stones_back():
                    s.rotate(self.rotx)
            elif chr == 'b':
                for s in self.stones_back():
                    s.rotate(-self.rotx)
        self.draw()

    def turn_cube(self, rot_mat):
        for s in self.stones:
            s.rotate(rot_mat)
        self.draw()


class CubeSolver:

    def __init__(self, cube):
        self.cube = cube

    '''
    def build_down_side(self) :
        wrong_stones = cube.get_wrong_edge_stones(SIDE_DIR_WHITE)
        for ws in wrong_edge_stones :
            if stone_on_side(ws, -SIDE_DIR_WHITE)
                while dist(ws.position, search_correct_stone(ws).position) != 2 : 
                    cube.turn_side('U')

                cs = search_correct_stone(ws)
                if 
                    (cs.faces[0].direction == SIDE_DIR_BLUE and cs.faces[0].color == SIDE_COL_WHITE) 
                    or
                    (cs.faces[1].direction == SIDE_DIR_BLUE and cs.faces[1].color == SIDE_COL_WHITE)
                    : 
                    cube.turn_side('ULrflR')
        '''


def main():
    # init graphics
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    ax.set_xlim(-2, 2)
    ax.set_ylim(-2, 2)
    ax.set_zlim(-2, 2)
    ax.azim = 0
    ax.elev = 20
    plt.plot([0, 3], [0, 0], [0, 0], '--k', color='b', linewidth=3)
    plt.plot([0, 0], [0, 3], [0, 0], '--k', color='r', linewidth=3)
    plt.plot([0, 0], [0, 0], [0, 3], '--k', color='y', linewidth=3)

    # init cube
    cube = Cube(ax)
    plt.show()

    # turn cube
    for x in range(0, 1):
        # cube.turn_cube(cube.rotx)
        cube.turn_side('u')
        ax.azim = x
        plt.show()


if __name__ == "__main__":
    main()
