def build_english_language_trie():
    f = open('/usr/share/dict/words', 'r')
    return build_trie(f.readlines())

def build_trie(word_list):
    root = Trie()
    for word in word_list:
        root.insert(word)
    return root

class Trie:

    def __init__(self):
        self.children = {}
        self.is_word = False

    def insert(self, word):
        word = word.lower().strip()

        if len(word) == 0:
            self.is_word = True
            return

        letter = word[0]
        rest_of_word = word[1:]

        if letter not in self.children:
            self.children[letter] = Trie()

        self.children[letter].insert(rest_of_word)

    def contains(self, word):
        word = word.lower()

        if len(word) == 0:
            return True, self.is_word

        letter = word[0]
        rest_of_word = word[1:]

        if letter in self.children:
            return self.children[letter].contains(rest_of_word)
        else:
            return False, False


