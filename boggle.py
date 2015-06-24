import random

class Boggle:
    size = 4
    dice = ["aaeegn", "abbjoo", "achops", "affkps",
            "aoottw", "cimotu", "deilrx", "delrvy",
            "distty", "eeghnw", "eeinsu", "ehrtvw",
            "eiosst", "elrtty", "himnqu", "hlnnrz"]

    directions = [(1, 0), (-1, 0), (0, 1), (1, 1),
                  (-1, 1), (0, -1), (1, -1), (-1, -1)]

    def __init__(self, board_str):
        self.grid = [['' for i in range(Boggle.size)] for j in range(Boggle.size)]
        dice_index = 0
        for x in range(0, Boggle.size):
            for y in range(0, Boggle.size):
                self.grid[x][y] = board_str[dice_index]
                dice_index += 1

    def __str__(self):
        result = ''
        for row in self.grid:
            result += '\t'.join(row) + '\n'
        return result

    def solve(self, word_trie):
        words = {}

        def dfs_solve(word_so_far, pos, path_so_far):

            # out of bounds
            if pos[0] < 0 or pos[0] >= Boggle.size or pos[1] < 0 or pos[1] >= Boggle.size:
                return

            # cycle
            if pos in path_so_far:
                return

            word_so_far = word_so_far + self.grid[pos[0]][pos[1]]
            is_substring, is_word = word_trie.contains(word_so_far)

            # dead path
            if not is_substring:
                return

            visited_so_far = path_so_far[:] + [pos]

            if is_word and len(word_so_far) >= 3:
                words[word_so_far] = visited_so_far[:]

            for d in Boggle.directions:
                new_pos = (pos[0] + d[0], pos[1] + d[1])
                dfs_solve(word_so_far, new_pos, visited_so_far)


        for x in range(0, Boggle.size):
            for y in range(0, Boggle.size):
                dfs_solve('', (x, y), [])
        return words

def random_board():
    board_str = ''
    dice_index = 0
    random.shuffle(Boggle.dice)
    for w in range(0, Boggle.size**2):
        board_str += random.choice(Boggle.dice[dice_index])
        dice_index += 1
    return Boggle(board_str)

def count_points(solutions):
    points = 0
    for word in solutions:
        letters = len(word)
        if letters <= 4:
            points += 1
        elif letters == 5:
            points += 2
        elif letters == 6:
            points += 3
        elif letters == 7:
            points += 5
        else:
            points += 8
    return points

