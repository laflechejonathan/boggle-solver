from trie import build_english_language_trie
from jinja2 import Environment, PackageLoader
from boggle import Boggle, random_board, count_points
from argparse import ArgumentParser

def main():
    parser = ArgumentParser(description="Solve a given boggle board")
    parser.add_argument("--board", dest="board", help="a list of 16 characters making up \
            the board - if not provided, this is generated randomly")
    args = parser.parse_args()

    if (args.board):
        board = Boggle(args.board)
    else:
        board = random_board()

    trie = build_english_language_trie()
    solutions = board.solve(trie)
    num_words = len(solutions)
    points = count_points(solutions)
    sorted_words = sorted(solutions.keys())

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

