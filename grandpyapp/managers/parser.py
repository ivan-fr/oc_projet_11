import json
from config import STOP_WORDS_FILE


class Parser:
    @staticmethod
    def get_words_from_sentence(sentence):
        """Get words from sentence."""
        cursor, i, sentence = 0, 0, sentence.strip().lower() + " "

        while i <= len(sentence) - 1:
            if not sentence[i].isalpha() and not sentence[i] == "'":
                if i - 1 >= cursor:
                    word = sentence[cursor:i]
                    if "'" in word:
                        word = word[word.index("'") + 1:]
                    yield word
                delta = 1
                while i + delta <= len(sentence) - 1:
                    if sentence[i + delta].isalpha():
                        break
                    delta += 1
                i = cursor = i + delta
            i += 1

    @staticmethod
    def parse_sentence(sentence):
        """Parse a sentence for get the words and
         from their words get the main asked place."""
        words = Parser.get_words_from_sentence(sentence)

        with open(STOP_WORDS_FILE, "r", encoding="utf-8") as file:
            stop_words = json.load(file)
            return ' '.join(word for word in words if word not in stop_words)
