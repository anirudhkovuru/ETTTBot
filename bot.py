import random
import sys
import copy
import math
import time

class D4C:
    def __init__(self):
        self.ply = 3
        self.num = 0
        self.cntp = 0
        self.cnto = 0

    def move(self, board, old_move, pflag):
        if old_move == (-1, -1):
            return (4*random.randint(1, 2) + random.randint(1, 2), 4*random.randint(1, 2) + random.randint(1, 2))

        startt = time.clock()

        if pflag == 'o':
            oflag = 'x'
        else:
            oflag = 'o'

        self.num += 1
        max_ply = 3

        for i in range(4):
            for j in range(4):
                if board.block_status[i][j] == pflag:
                    self.cntp += 1
                elif board.block_status[i][j] == oflag:
                    self.cnto += 1

        if self.cnto - self.cntp > 1 or self.num > 25 or self.cntp == 2:
            self.ply = max_ply

        dum_board = copy.deepcopy(board)

        next_move = self.minimax(old_move, 0, True, -sys.maxint, sys.maxint, pflag, oflag, (-1, -1), dum_board)[1]

        elapsed = (time.clock() - startt)

        #print elapsed

        return next_move

    def update(self, dum_board, pflag, move):
        temp_board = copy.deepcopy(dum_board)
        x = move[0]/4
        y = move[1]/4
        bs = temp_board.board_status

        #checking if a block has been won or drawn or not after the current move
        for i in range(4):

            #checking for horizontal pattern(i'th row)
            if (bs[4*x+i][4*y] == bs[4*x+i][4*y+1] == bs[4*x+i][4*y+2] == bs[4*x+i][4*y+3]) and (bs[4*x+i][4*y] == pflag):
                temp_board.block_status[x][y] = pflag
                return temp_board

            #checking for vertical pattern(i'th column)
            if (bs[4*x][4*y+i] == bs[4*x+1][4*y+i] == bs[4*x+2][4*y+i] == bs[4*x+3][4*y+i]) and (bs[4*x][4*y+i] == pflag):
                temp_board.block_status[x][y] = pflag
                return temp_board

        #checking for diamond pattern
        #diamond 1
        if (bs[4*x+1][4*y] == bs[4*x][4*y+1] == bs[4*x+2][4*y+1] == bs[4*x+1][4*y+2]) and (bs[4*x+1][4*y] == pflag):
            temp_board.block_status[x][y] = pflag
            return temp_board

        #diamond 2
        if (bs[4*x+1][4*y+1] == bs[4*x][4*y+2] == bs[4*x+2][4*y+2] == bs[4*x+1][4*y+3]) and (bs[4*x+1][4*y+1] == pflag):
            temp_board.block_status[x][y] = pflag
            return temp_board

        #diamond 3
        if (bs[4*x+2][4*y] == bs[4*x+1][4*y+1] == bs[4*x+3][4*y+1] == bs[4*x+2][4*y+2]) and (bs[4*x+2][4*y] == pflag):
            temp_board.block_status[x][y] = pflag
            return temp_board

        #diamond 4
        if (bs[4*x+2][4*y+1] == bs[4*x+1][4*y+2] == bs[4*x+3][4*y+2] == bs[4*x+2][4*y+3]) and (bs[4*x+2][4*y+1] == pflag):
            temp_board.block_status[x][y] = pflag
            return temp_board

        #checking if a block has any more cells left or has it been drawn
        for i in range(4):
            for j in range(4):
                if bs[4*x+i][4*y+j] == '-':
                    return temp_board
        temp_board.block_status[x][y] = 'd'
        return temp_board

    def minimax(self, old_move, depth, maximizingPlayer, alpha, beta, pflag, oflag, best_move, dum_board):

        if depth == self.ply:
            score = self.evaluate_global(pflag, oflag, dum_board)
            return (score, best_move)
        else:
            moves = dum_board.find_valid_move_cells(old_move)

            if len(moves) == 0:
                score = self.evaluate_global(pflag, oflag, dum_board)
                score = round(score, 4)
                self.ply = max(depth, 1)
                return (score, old_move)

            if depth == 0:
                if len(moves) > 17:
                    self.ply = min(self.ply, 1)

            for move in moves:

                if maximizingPlayer:
                    dum_board.board_status[move[0]][move[1]] = pflag
                else:
                    dum_board.board_status[move[0]][move[1]] = oflag

                temp_board = self.update(dum_board, pflag, move)

                if maximizingPlayer:
                    val = self.minimax(move, depth + 1, False, alpha, beta, pflag, oflag, best_move, temp_board)[0]
                    val = round(val, 4)
                    if val > alpha:
                        alpha = val
                        best_move = move

                else:
                    val = self.minimax(move, depth + 1, True, alpha, beta, pflag, oflag, best_move, temp_board)[0]
                    val = round(val, 4)
                    if val < beta:
                        beta = val
                        best_move = move

                dum_board.board_status[move[0]][move[1]] = '-'

                if alpha > beta:
                    break

            if depth == 0:
                if best_move[0] == -1 or best_move[1] == -1:
                    best_move = moves[0]

            if maximizingPlayer:
                return (alpha, best_move)
            else:
                return (beta, best_move)

    def evaluate_global(self, pflag, oflag, dum_board):
        blocks = dum_board.block_status
        hvalues = [[0 for k in range(4)] for i in range(4)]
        gain = 0
        lim = 1000.0

        for i in range(4):
            for j in range(4):
                hvalues[i][j] = self.evaluate_local(i, j, pflag, dum_board)*self.get_points(i, j)
                hvalues[i][j] /= lim

        for i in range(4):
            p = 0
            cp = 0
            ce = 0
            for j in range(4):
                p += hvalues[i][j]
                if blocks[i][j] == pflag:
                    cp += 1
                elif blocks[i][j] == oflag:
                    ce += 1
            gain = self.case_eval(p, gain)
            gain = self.win_loss_cond_global(cp, ce, gain)

        for i in range(4):
            p = 0
            cp = 0
            ce = 0
            for j in range(4):
                p += hvalues[j][i]
                if blocks[j][i] == pflag:
                    cp += 1
                elif blocks[j][i] == oflag:
                    ce += 1
            gain = self.case_eval(p, gain)
            gain = self.win_loss_cond_global(cp, ce, gain)

        p = 0
        cp = 0
        ce = 0

        #diamond 1

        p += hvalues[1][0]
        if(blocks[1][0] == pflag):
            cp += 1
        elif(blocks[1][0] == oflag):
            ce += 1

        p += hvalues[0][1]
        if(blocks[0][1] == pflag):
            cp += 1
        elif(blocks[0][1] == oflag):
            ce += 1

        p += hvalues[2][1]
        if(blocks[2][1] == pflag):
            cp += 1
        elif(blocks[2][1] == oflag):
            ce += 1

        p += hvalues[1][2]
        if(blocks[1][2] == pflag):
            cp += 1
        elif(blocks[1][2] == oflag):
            ce += 1

        gain = self.case_eval(p, gain)
        gain = self.win_loss_cond_global(cp, ce, gain)

        p = 0
        cp = 0
        ce = 0

        #diamond 2

        p += hvalues[1][1]
        if(blocks[1][1] == pflag):
            cp += 1
        elif(blocks[1][1] == oflag):
            ce += 1

        p += hvalues[0][2]
        if(blocks[0][2] == pflag):
            cp += 1
        elif(blocks[0][2] == oflag):
            ce += 1

        p += hvalues[2][2]
        if(blocks[2][2] == pflag):
            cp += 1
        elif(blocks[2][2] == oflag):
            ce += 1

        p += hvalues[1][3]
        if(blocks[1][3] == pflag):
            cp += 1
        elif(blocks[1][3] == oflag):
            ce += 1

        gain = self.case_eval(p, gain)
        gain = self.win_loss_cond_global(cp, ce, gain)

        p = 0
        cp = 0
        ce = 0

        #diamond 3

        p += hvalues[2][0]
        if(blocks[2][0] == pflag):
            cp += 1
        elif(blocks[2][0] == oflag):
            ce += 1

        p = hvalues[1][1]
        if(blocks[1][1] == pflag):
            cp += 1
        elif(blocks[1][1] == oflag):
            ce += 1

        p += hvalues[3][1]
        if(blocks[3][1] == pflag):
            cp += 1
        elif(blocks[3][1] == oflag):
            ce += 1

        p += hvalues[2][2]
        if(blocks[2][2] == pflag):
            cp += 1
        elif(blocks[2][2] == oflag):
            ce += 1

        gain = self.case_eval(p, gain)
        gain = self.win_loss_cond_global(cp, ce, gain)

        p = 0
        cp = 0
        ce = 0

        #diamond 4

        p += hvalues[2][1]
        if(blocks[2][1] == pflag):
            cp += 1
        elif(blocks[2][1] == oflag):
            ce += 1

        p += hvalues[1][2]
        if(blocks[1][2] == pflag):
            cp += 1
        elif(blocks[1][2] == oflag):
            ce += 1

        p += hvalues[3][2]
        if(blocks[3][2] == pflag):
            cp += 1
        elif(blocks[3][2] == oflag):
            ce += 1

        p += hvalues[2][3]
        if(blocks[2][3] == pflag):
            cp += 1
        elif(blocks[2][3] == oflag):
            ce += 1

        gain = self.case_eval(p, gain)
        gain = self.win_loss_cond_global(cp, ce, gain)

        if self.cntp < 2:
            if blocks[1][1] == pflag or blocks[2][2] == pflag or blocks[1][2] == pflag or blocks[2][1] == pflag:
                gain += 10
            elif blocks[1][1] != '-' or blocks[2][2] != '-' or blocks[1][2] != '-' or blocks[2][1] != '-':
                gain -= 10

        cnt1 = 0
        cnt2 = 0
        for i in range(4):
            for j in range(4):
                if blocks[i][j] == pflag:
                    cnt1 += 1
                elif blocks[i][j] == oflag:
                    cnt2 += 2
        if self.cntp < cnt1 and cnt2 == self.cnto:
            gain += 50
        elif cnt1 > self.cntp and (cnt1 - self.cntp) < (cnt2 - self.cnto):
            gain -= 20
        elif cnt1 < self.cntp and cnt2 > self.cnto:
            gain -= 50

        return gain


    def get_points(self, x, y):
        if (x == 0 or x == 3) and (y == 0 or y == 3):
            m = 6
        elif (x == 1 or x == 2) and (y == 1 or y == 2):
            m = 3
        else:
            m = 4
        return m

    def evaluate_local(self, x, y, pflag, dum_board):
        gain = 0
        bs = dum_board.board_status

        for i in range(4):
            cp = 0
            cd = 0
            ce = 0
            for j in range(4):
                if bs[4*x + i][4*y + j] == '-':
                    cd += 1
                elif bs[4*x + i][4*y + j] == pflag:
                    cp += 1
                else:
                    ce += 1
            gain = self.win_loss_cond(cp, ce, gain)

        for i in range(4):
            cp = 0
            cd = 0
            ce = 0
            for j in range(4):
                if bs[4*x + j][4*y + i] == '-':
                    cd += 1
                elif bs[4*x + j][4*y + i] == pflag:
                    cp += 1
                else:
                    ce += 1
            gain = self.win_loss_cond(cp, ce, gain)

        cp = 0
        cd = 0
        ce = 0

        #diamond 1

        if(bs[4*x + 1][4*y] == pflag):
            cp += 1
        elif(bs[4*x + 1][4*y] == '-'):
            cd += 1
        else:
            ce += 1

        if(bs[4*x][4*y + 1] == pflag):
            cp += 1
        elif(bs[4*x][4*y + 1] == '-'):
            cd += 1
        else:
            ce += 1


        if(bs[4*x + 2][4*y + 1] == pflag):
            cp += 1
        elif(bs[4*x + 2][4*y + 1] == '-'):
            cd += 1
        else:
            ce += 1

        if(bs[4*x + 1][4*y + 2] == pflag):
            cp += 1
        elif(bs[4*x + 1][4*y + 2] == '-'):
            cd += 1
        else:
            ce += 1

        gain = self.win_loss_cond(cp, ce, gain)

        cp = 0
        cd = 0
        ce = 0

        #diamond 2

        if(bs[4*x + 1][4*y + 1] == pflag):
            cp += 1
        elif(bs[4*x + 1][4*y + 1] == '-'):
            cd += 1
        else:
            ce += 1

        if(bs[4*x][4*y + 2] == pflag):
            cp += 1
        elif(bs[4*x][4*y + 2] == '-'):
            cd += 1
        else:
            ce += 1

        if(bs[4*x + 2][4*y + 2] == pflag):
            cp += 1
        elif(bs[4*x + 2][4*y + 2] == '-'):
            cd += 1
        else:
            ce += 1

        if(bs[4*x + 1][4*y + 3] == pflag):
            cp += 1
        elif(bs[4*x + 1][4*y + 3] == '-'):
            cd += 1
        else:
            ce += 1

        gain = self.win_loss_cond(cp, ce, gain)

        cp = 0
        cd = 0
        ce = 0

        #diamond 3

        if(bs[4*x + 2][4*y] == pflag):
            cp += 1
        elif(bs[4*x + 2][4*y] == '-'):
            cd += 1
        else:
            ce += 1

        if(bs[4*x + 1][4*y + 1] == pflag):
            cp += 1
        elif(bs[4*x + 1][4*y + 1] == '-'):
            cd += 1
        else:
            ce += 1

        if(bs[4*x + 3][4*y + 1] == pflag):
            cp += 1
        elif(bs[4*x + 3][4*y + 1] == '-'):
            cd += 1
        else:
            ce += 1

        if(bs[4*x + 2][4*y + 2] == pflag):
            cp += 1
        elif(bs[4*x + 2][4*y + 2] == '-'):
            cd += 1
        else:
            ce += 1

        gain = self.win_loss_cond(cp, ce, gain)

        cp = 0
        cd = 0
        ce = 0

        #diamond 4

        if(bs[4*x + 2][4*y + 1] == pflag):
            cp += 1
        elif(bs[4*x + 2][4*y + 1] == '-'):
            cd += 1
        else:
            ce += 1

        if(bs[4*x + 1][4*y + 2] == pflag):
            cp += 1
        elif(bs[4*x + 1][4*y + 2] == '-'):
            cd += 1
        else:
            ce += 1

        if(bs[4*x + 3][4*y + 2] == pflag):
            cp += 1
        elif(bs[4*x + 3][4*y + 2] == '-'):
            cd += 1
        else:
            ce += 1

        if(bs[4*x + 2][4*y + 3] == pflag):
            cp += 1
        elif(bs[4*x + 2][4*y + 3] == '-'):
            cd += 1
        else:
            ce += 1

        gain = self.win_loss_cond(cp, ce, gain)

        return gain

    def win_loss_cond(self, cp, ce, gain):
        if cp > 0:
            gain += pow(10, cp-1)
        if ce > 0:
            gain -= pow(10, ce-1)
        return gain

    def case_eval(self, p, gain):
        #the heuristic main function goes here
        if p >= -6 and p < 3:
            gain += p

        if p >= 3 and p < 7:
            val = 1
            val += (p - 3) * 3
            gain += val

        if p >= 7 and p < 13:
            val = 10
            val += (p - 7) * 18
            gain += val

        if p >= 13 and p < 17:
            val = 100
            val += (p - 13) * 300
            gain += val

        if p >= 17 and p < 21:
            val = 1000
            val += (p - 17) * 3000
            gain += val

        if p < -6 and p >= -10:
            val = -10
            val -= (abs(p) - 6) * 22.5
            gain += val

        if p < -10 and p >= -16:
            val = -100
            val -= (abs(p) - 10) * 150
            gain += val

        if p < -16 and p >= -20:
            val = -1000
            val -= (abs(p) - 16) * 2250
            gain += val

        return gain

    def win_loss_cond_global(self, cp, ce, gain):
        if cp > 0:
            gain += pow(10, cp)
        if ce > 0:
            gain -= pow(10, ce)
        return gain
