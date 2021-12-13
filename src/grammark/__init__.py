import json
import re

def load_json(filename):
    """Loads a json object from the file with given filename
    """
    data = None

    with open(filename) as f:
        data = json.load(f)

    return data

class TextData:
    def __init__(self, text):
        self.text = text
        self.word_values = self.lex(text)

    def lex(self, text):
        """Lexes the text. Splits it into a list of single words,
        that are annotated with start and end indices. Also a
        sentence index is added to differentiate sentences in the text.
        """
        # replace ; by .
        text = re.sub(r';', '.', text)
        ret_val = []
        sentence_count = 0
        index = 0

        text_len = len(text)

        while index < text_len:
            while text[index] == " " and index < text_len:
                index += 1

            if index >= text_len:
                break

            start_pos = index

            while text[index] not in " ,.!?:-\n'\")({}":
                index += 1

            ret_val.append({"start_pos" : start_pos, "end_pos": index, "sentence": sentence_count})

            if text[index] in ".?!":
                sentence_count += 1

            index += 1

        return ret_val

def check_passive_voice(text):
    """Checks the given text for passive voice in accordance to grammark

    Return:
    {
        "score": <score>,
        "findings": [{ "start_pos": <index>, "end_pos": <index>, "remark" : <remark/correction/None> }]
    }

    start_pos: is the start position of the problematic fragment
    end_pos: is the end position of the problematic fragment
    remark: can be a remark, a proposed correction or None if there is no such thing
    """
    pass

def check_wordiness(text):
    pass

def check_normalizations(text):
    pass

def check_sentences(text):
    pass

def check_transitions(text):
    pass

def check_academic(text):
    pass

def check_grammar(text):
    pass

def check_eggcorns(text):
    pass
