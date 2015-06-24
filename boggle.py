import random
from trie import build_english_language_trie
from jinja2 import Environment, PackageLoader


class Boggle:
    size = 4
    dice = ["aaeegn", "abbjoo", "achops", "affkps",
            "aoottw", "cimotu", "deilrx", "delrvy",
            "distty", "eeghnw", "eeinsu", "ehrtvw",
            "eiosst", "elrtty", "himnqu", "hlnnrz"]

    directions = [(1, 0), (-1, 0), (0, 1), (1, 1),
                  (-1, 1), (0, -1), (1, -1), (-1, -1)]

    def __init__(self):
        self.grid = [['' for i in range(Boggle.size)] for j in range(Boggle.size)]
        dice_index = 0
        random.shuffle(Boggle.dice)
        for x in range(0, Boggle.size):
            for y in range(0, Boggle.size):
                letter = random.choice(Boggle.dice[dice_index])
                self.grid[x][y] = letter
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

def main():
    trie = build_english_language_trie()
    board = Boggle()
    solutions = board.solve(trie)
    num_words = len(solutions)
    points = count_points(solutions)
    sorted_words = sorted(solutions.keys())

    #print board
    #print '\n'.join(solutions)
    #print '%d words, for a total of %d points' % (num_words, points)

    # render report to HTML
    env = Environment(loader=PackageLoader('boggle', 'templates'))
    template = env.get_template('report.html')

    # setup solutions for render:
    formatted_solutions = {}
    for word in solutions:
        formatted_pos = ['%d-%d' % pos for pos in solutions[word]]
        formatted_solutions[word] = formatted_pos

    output = template.render(grid=board.grid, solutions=formatted_solutions, num_words=num_words, points=points, sorted_words=sorted_words, size=Boggle.size)
    print output

if __name__ == "__main__":
    main()
