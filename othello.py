# -*- coding: utf-8 -*-
"""
@author: phd_mech
"""

import sys
import numpy as np
import matplotlib.pyplot as plt

def show_mat():
    """
    draw game board
    """
    num_b = np.sum(MAT == B)
    num_w = np.sum(MAT == W)
    plt.rcParams['axes.facecolor'] = 'g'
    plt.rcParams['text.color'] = 'w'
    plt.rcParams['xtick.color'] = 'w'
    plt.rcParams['ytick.color'] = 'w'
    line_width = 2
    plt.figure(figsize=(6, 6), facecolor='k')
    plt.subplot(111)
    plt.title('Black:White = {}:{}'.format(num_b, num_w))
    for y_pos in range(SIZE):
        plt.axhline(y_pos-.5, color='k', lw=line_width)
        for x_pos in range(SIZE):
            plt.axvline(x_pos-.5, color='k', lw=line_width)
            if MAT[y_pos, x_pos] == B:
                plt.plot(x_pos, y_pos, 'o', color='k', ms=30)
            elif MAT[y_pos, x_pos] == W:
                plt.plot(x_pos, y_pos, 'o', color='w', ms=30)
    plt.xlim([-.5, SIZE-.5])
    plt.ylim([-.5, SIZE-.5])
    plt.gca().set_aspect('equal', adjustable='box')
    plt.tick_params(length=0)
    plt.tight_layout()
    plt.show()

def fin_pos(x_pos, y_pos, my_color, opp_color, flip):
    """
    find flippable positions
    """
    if not (0 <= y_pos < SIZE) and (0 <= x_pos < SIZE):
        return False
    if MAT[y_pos, x_pos] != 0:
        return False
    for direction in CHECK_DIRECTION:
        y_check = y_pos
        x_check = x_pos
        y_check += direction[0]
        x_check += direction[1]
        if (0 <= y_check < SIZE) and (0 <= x_check < SIZE):
            if MAT[y_check, x_check] == opp_color:
                while True:
                    y_check += direction[0]
                    x_check += direction[1]
                    if not (0 <= y_check < SIZE) and (0 <= x_check < SIZE):
                        break
                    if MAT[y_check, x_check] == 0:
                        break
                    if MAT[y_check, x_check] == my_color:
                        if not flip:
                            return True
                        y_flip = y_pos
                        x_flip = x_pos
                        while True:
                            MAT[y_flip, x_flip] = my_color
                            y_flip += direction[0]
                            x_flip += direction[1]
                            if (y_flip == y_check) and (x_flip == x_check):
                                break
    return False

def fin_pos_all(my_color, opp_color):
    """
    find all flippable positions
    """
    for y_pos in range(SIZE):
        for x_pos in range(SIZE):
            if fin_pos(x_pos, y_pos, my_color, opp_color, False):
                return True
    return False

def input_position(color_name):
    """
    select position
    """
    while True:
        keys = input('x,y=')
        if keys == 'q':
            sys.exit('See you again!!')
        try:
            x_pos, y_pos = map(int, keys.split(','))
            return x_pos, y_pos
        except:
            print('Type error (Quit => Type "q")')
            print('{} turn.'.format(color_name), end='')

def victordefeat():
    """
    judgement
    """
    num_b = np.sum(MAT == B)
    num_w = np.sum(MAT == W)
    print('Black:{}, White:{}'.format(str(num_b), num_w))
    if num_b == num_w:
        print('Draw')
    elif num_b > num_w:
        print('Black win')
    elif num_b < num_w:
        print('White win')

def main():
    """
    main program
    """
    MAT[CENTER-1, CENTER-1:CENTER+1] = np.array([W, B])
    MAT[CENTER, CENTER-1:CENTER+1] = np.array([B, W])
    show_mat()
    turn = 0
    unavailable = False
    while True:
        color = COLORS[turn]  # define tunr color
        color_name = COLOR_NAMES[turn]  # define turn name
        if unavailable:
            print('\nCannot select (Quit => Type "q")')
            print('\n{} turn.'.format(color_name), end='')
        else:
            print('{} turn.'.format(color_name), end='')
        unavailable = False
        x_pos, y_pos = input_position(color_name)
        if not fin_pos(x_pos, y_pos, COLORS[turn], COLORS[turn^1], False):
            unavailable = True
        else:
            fin_pos(x_pos, y_pos, COLORS[turn], COLORS[turn^1], True)
            MAT[y_pos, x_pos] = color
            show_mat()
            turn ^= 1
        if not fin_pos_all(B, W) and not fin_pos_all(W, B):
            print('Game set')
            break
        if not fin_pos_all(COLORS[turn], COLORS[turn^1]):
            turn ^= 1
            print('Pass')
    victordefeat()

if __name__ == '__main__':
    SIZE = 8
    CENTER = SIZE//2
    B, W = 1, 2
    COLORS = [B, W]
    COLOR_NAMES = ['Black', 'White']
    CHECK_DIRECTION = np.array([[-1, -1], [-1, 0], [-1, 1],
                                [0, -1], [0, 1],
                                [1, -1], [1, 0], [1, 1]])
    MAT = np.zeros([SIZE, SIZE])
    main()
