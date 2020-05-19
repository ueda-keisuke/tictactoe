import copy
import random_bot

class State:
    def __init__(self, player = 1, board = None):
        # オリジナルではビットマスクを使っているけど、ここでは配列を使う
        # 0, なにもない
        # 1, ○
        # -1; ✗
        if board is None:
            self.board = [
                [0, 0, 0],
                [0, 0, 0],
                [0, 0, 0],
            ]
        else:
            self.board = copy.deepcopy(board)

        # 最初のプレーヤーは1, 敵は-1
        self.player = player


    # Trueのときは負けている
    def lose(self):
        enemy_id = self.player * -1

        # 横が揃っている
        if self.board[0][0] == enemy_id and self.board[0][1] == enemy_id and self.board[0][2] == enemy_id:
            return True
        if self.board[1][0] == enemy_id and self.board[1][1] == enemy_id and self.board[1][2] == enemy_id:
            return True
        if self.board[2][0] == enemy_id and self.board[2][1] == enemy_id and self.board[2][2] == enemy_id:
            return True

        # 縦
        if self.board[0][0] == enemy_id and self.board[1][0] == enemy_id and self.board[2][0] == enemy_id:
            return True
        if self.board[0][1] == enemy_id and self.board[1][1] == enemy_id and self.board[2][1] == enemy_id:
            return True
        if self.board[0][2] == enemy_id and self.board[1][2] == enemy_id and self.board[2][2] == enemy_id:
            return True

        # 斜め
        if self.board[0][0] == enemy_id and self.board[1][1] == enemy_id and self.board[2][2] == enemy_id:
            return True
        if self.board[0][2] == enemy_id and self.board[1][1] == enemy_id and self.board[2][0] == enemy_id:
            return True

        return False

    def draw(self):
        # 全部埋まっていて勝ち負けがついていないときは引き分け
        count = 0
        for r in self.board:
            for c in r:
                if c != 0:
                    count += 1

        if count == 9:
            return True
        else:
            return False

    def end(self):
        return self.lose() or self.draw()

    # 着手可能点のtupleを返す
    def legal_moves(self):
        array = []
        for r in range(0, len(self.board)):
            for c in range(0, len(self.board[r])):
                if self.board[r][c] == 0:
                    array.append((r, c))

        return tuple(array)

    # 着手して次のstateを返す
    def move(self, point):
        row = point[0]
        col = point[1]

        if self.board[row][col] != 0:
            raise Exception
        else:
            next_board = copy.deepcopy(self.board)
            next_board[row][col] = self.player

            # 敵と味方を入れ替える
            return State(self.player * -1, next_board)

    def print_board(self):
        print("-----------------------")
        for r in self.board:
            for c in r:
                icon = "\t"
                if c == 1:
                    icon = "○\t"
                elif c == -1:
                    icon = "✗\t"
                print(icon, end="")
            print("")




def main():
    state = State()
    flag = state.end()
    while flag == False:
        legal_moves = state.legal_moves()
        state = state.move(random_bot.choice(legal_moves))
        state.print_board()
        flag = state.end()


if __name__ == '__main__':
    main()