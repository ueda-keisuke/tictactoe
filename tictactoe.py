# http://tail-island.github.io/programming/2018/06/15/min-max-alpha-beta.html

from funcy import *
from math import inf
from random import randint


def _popcount(x):
    return bin(x).count('1')  # Pythonだと、コレが手軽で速いらしい。


# ゲームの状態。
class State:
    def __init__(self, pieces=0, enemy_pieces=0):
        self.pieces = pieces
        self.enemy_pieces = enemy_pieces

    @property
    def lose(self):
        return any(lambda mask: self.enemy_pieces & mask == mask, (
        0b111000000, 0b000111000, 0b000000111, 0b100100100, 0b010010010, 0b001001001, 0b100010001, 0b001010100))

    @property
    def draw(self):
        return _popcount(self.pieces) + _popcount(self.enemy_pieces) == 9

    @property
    def end(self):
        return self.lose or self.draw

    @property
    def legal_actions(self):
        return tuple(
            i for i in range(9) if not self.pieces & 0b100000000 >> i and not self.enemy_pieces & 0b100000000 >> i)

    def next(self, action):
        return State(self.enemy_pieces, self.pieces | 0b100000000 >> action)

    def __str__(self):
        ox = ('o', 'x') if _popcount(self.pieces) == _popcount(self.enemy_pieces) else ('x', 'o')
        return '\n'.join(''.join((ox[0] if self.pieces & 0b100000000 >> i * 3 + j else None) or (
            ox[1] if self.enemy_pieces & 0b100000000 >> i * 3 + j else None) or '-' for j in range(3)) for i in
                         range(3))


# ランダムで次の手を返します。
def random_next_action(state):
    return state.legal_actions[randint(0, len(state.legal_actions) - 1)]


# ミニ・マックス法（正確にはネガ・マックス法）
def nega_max(state):
    if state.lose:
        return -1

    if state.draw:
        return 0

    best_score = -inf

    for action in state.legal_actions:
        score = -nega_max(state.next(action))

        if score > best_score:
            best_score = score

    return best_score


# 次の手を返します（nega_maxはスコアを返すので、手を返すようにするためにほぼ同じ関数が必要になっちゃいました）。
def nega_max_next_action(state):
    best_score = -inf

    for action in state.legal_actions:
        score = -nega_max(state.next(action))

        if score > best_score:
            best_action = action
            best_score = score

    return best_action


# アルファ・ベータ法（正確にはネガ・アルファ法）
def nega_alpha(state, alpha, beta):
    if state.lose:
        return -1

    if state.draw:
        return 0

    for action in state.legal_actions:
        score = -nega_alpha(state.next(action), -beta, -alpha)

        if score > alpha:
            alpha = score

        if alpha >= beta:
            return alpha

    return alpha


# 次の手を返します（nega_alphaはスコアを返すので、手を返すようにするためにほぼ同じ関数が必要になっちゃいました）。
def nega_alpha_next_action(state):
    alpha = -inf

    for action in state.legal_actions:
        score = -nega_alpha(state.next(action), -inf, -alpha)

        if score > alpha:
            best_action = action
            alpha = score

    return best_action


def main():
    state = State()

    for next_action in cat(repeat((nega_alpha_next_action,
                                   nega_max_next_action))):  # random_next_action, nega_max_next_action, nega_alpha_next_actionの中から適当に選んでください
        if state.end:
            break;

        state = state.next(next_action(state))

        print(state)
        print()


if __name__ == '__main__':
    main()
