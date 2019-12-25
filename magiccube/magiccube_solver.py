import msvcrt as ms
import numpy as np
import matplotlib.pyplot as plt
import math as m
from mpl_toolkits.mplot3d import Axes3D
from mpl_toolkits.mplot3d.art3d import Poly3DCollection, Line3DCollection
import time as t

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

SIDE_DIR_RIGHT = (0, 1, 0)
SIDE_DIR_LEFT = (0, -1, 0)
SIDE_DIR_BACK = (-1, 0, 0)
SIDE_DIR_FRONT = (1, 0, 0)
SIDE_DIR_UP = (0, 0, 1)
SIDE_DIR_DOWN = (0, 0, -1)

SIDE_DIRS = np.array([SIDE_DIR_RIGHT, SIDE_DIR_LEFT, SIDE_DIR_BACK, SIDE_DIR_FRONT, SIDE_DIR_UP, SIDE_DIR_DOWN])


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

    def stones_side(self, side):
        y = np.array([])
        for s in self.stones:
            if np.dot(s.position, side) == 1: y = np.append(y, s)
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
                for s in self.stones_side(SIDE_DIR_RIGHT):
                    s.rotate(self.roty_)
            elif chr == 'r':
                for s in self.stones_side(SIDE_DIR_RIGHT):
                    s.rotate(self.roty)
            elif chr == 'L':
                for s in self.stones_side(SIDE_DIR_LEFT):
                    s.rotate(self.roty)
            elif chr == 'l':
                for s in self.stones_side(SIDE_DIR_LEFT):
                    s.rotate(self.roty_)
            elif chr == 'U':
                for s in self.stones_side(SIDE_DIR_UP):
                    s.rotate(self.rotz)
            elif chr == 'u':
                for s in self.stones_side(SIDE_DIR_UP):
                    s.rotate(self.rotz_)
            elif chr == 'D':
                for s in self.stones_side(SIDE_DIR_DOWN):
                    s.rotate(self.rotz)
            elif chr == 'd':
                for s in self.stones_side(SIDE_DIR_DOWN):
                    s.rotate(self.rotz_)
            elif chr == 'F':
                for s in self.stones_side(SIDE_DIR_FRONT):
                    s.rotate(self.rotx)
            elif chr == 'f':
                for s in self.stones_side(SIDE_DIR_FRONT):
                    s.rotate(self.rotx_)
            elif chr == 'B':
                for s in self.stones_side(SIDE_DIR_BACK):
                    s.rotate(self.rotx)
            elif chr == 'b':
                for s in self.stones_side(SIDE_DIR_BACK):
                    s.rotate(self.rotx_)
        self.draw()

    def turn_cube(self, rot_mat):
        for s in self.stones:
            s.rotate(rot_mat)
        self.draw()

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
                for f in s.faces:
                    if np.dot(f.direction, side) == 1 and f.color != self.get_color_of_side(side): ws = np.append(ws, s)
        return ws

    def get_correct_stone(self, ws):
        target_face_colors = np.array([])
        for f in ws.faces:
            target_face_colors = np.append(target_face_colors, self.get_color_of_side(f.direction))
        print('current colors: ', ws.faces[0].color, ws.faces[1].color)
        print('target colors: ', target_face_colors)

        for s in self.stones:
            if s.faces.size == target_face_colors.size:
                stone_face_colors = np.array([])
                for f in s.faces: stone_face_colors = np.append(stone_face_colors, f.color)
                print('target face colors: ', target_face_colors)
                print('stone face colors : ', stone_face_colors)
                if np.union1d(target_face_colors, stone_face_colors).size == target_face_colors.size:
                    return s


class CubeSolver:

    def __init__(self, cube):
        self.cube = cube

    def build_down_side(self):
        wrong_edge_stones = self.cube.get_wrong_edge_stones(self.cube.get_side_of_color(SIDE_COL_WHITE))
        print('number of wrong stones at white side: ', wrong_edge_stones.size)
        for ws in wrong_edge_stones:
            cs = self.cube.get_correct_stone(ws)
            cp = ws.position
            if self.cube.stone_on_side(cs, self.cube.get_side_of_color(SIDE_COL_YELLOW)):
                # print(np.linalg.norm(cp, cs.position))
                while np.dot(cp, cs.position) != 0:
                    self.cube.turn_side('U')
                self.cube.turn_side('ULrflR')


def main():
    # init graphics
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    ax.set_xlim(-2, 2)
    ax.set_ylim(-2, 2)
    ax.set_zlim(-2, 2)
    ax.azim = 10
    ax.elev = 20
    ax.plot([0, 3], [0, 0], [0, 0], '--k', color='b', linewidth=3)
    ax.plot([0, 0], [0, 3], [0, 0], '--k', color='r', linewidth=3)
    ax.plot([0, 0], [0, 0], [0, 3], '--k', color='y', linewidth=3)

    # init cube
    cube = Cube(ax)
    fig.show()

    # turn sides
    cube.turn_side('FFUrLrrbFllRudlRflflfl')
    fig.show()
    fig.canvas.flush_events()

    t.sleep(1)

    cube_solver = CubeSolver(cube)
    cube_solver.build_down_side()
    fig.show()
    fig.canvas.flush_events()
    ''' ''
    t.sleep(5)

    cube.turn_side('U')
    fig.show()
    fig.canvas.flush_events()

    t.sleep(2)
    cube.turn_side('L')
    fig.show()
    fig.canvas.flush_events()
    t.sleep(2)
    cube.turn_side('r')
    fig.show()
    fig.canvas.flush_events()

    t.sleep(2)
    cube.turn_side('f')
    fig.show()
    fig.canvas.flush_events()

    t.sleep(2)
    cube.turn_side('l')
    fig.show()
    fig.canvas.flush_events()
    t.sleep(2)
    cube.turn_side('R')
    fig.show()
    fig.canvas.flush_events()
    '''

    print('end')


if __name__ == "__main__":
    main()