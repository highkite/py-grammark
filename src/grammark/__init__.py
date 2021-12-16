try:
    import importlib.resources as pkg_resources
except ImportError:
    # Try backported to PY<37 `importlib_resources`.
    import importlib_resources as pkg_resources

import resources

import json
import re

ACADEMIC = None
EGGCORNS = None
GRAMMAR = None
HELPERS = None
IRREGULARS = None
NOMINALIZATION_POSTFIXES = None
SENTENCES_STARTS = None
TRANSITIONS = None
WORDINESS_WORDS = None

WORD_SEP = "[\-\/#!\"%\^&\*:{}=\-_`~()\s\.\,]"
WORD_START = "(^|" + WORD_SEP + ")("
WORD_END = ")(" + WORD_SEP + "|$)"

def load_json(filename):
    """Loads a json object from the file with given filename
    """
    data = json.loads(pkg_resources.read_text(resources, str(filename)))

    return data

class TextData:
    def __init__(self, text):
        self.text = text
        self.word_values = self.lex(text)

    def get_word_count(self):
        """Returns the total number of words
        """
        return len(self.word_values)

    def get_word(self, i):
        """Returns the i'th word or None if the index is out of range
        """
        if i > self.get_word_count():
            return None
        word_data = self.word_values[i]
        return self.text[word_data["start_pos"]:word_data["end_pos"]]

    def get_sentence_count(self):
        """Returns the number of sentences
        """
        return self.word_values[-1]["sentence"] + 1

    def find_substring(self, substring):
        """Finds the substring in the text and returns the indices
        """
        values = [{"start_pos": m.start(2), "end_pos": m.end(2), "sentence": None} for m in re.finditer(WORD_START + substring + WORD_END, self.text)]

        # look also for leading upper values
        capital_substring = substring[0].upper() + substring[1:]
        values += [{"start_pos": m.start(2), "end_pos": m.end(2), "sentence": None} for m in re.finditer(WORD_START + capital_substring + WORD_END, self.text)]

        return values

    def find_substring_set(self, substring_set):
        """Finds the substrings in the set in the text
        """
        ret_val = []

        for sbstr in substring_set:
            ret_val += self.find_substring(sbstr)

        return ret_val

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
            while index < text_len and text[index] == " ":
                index += 1

            if index >= text_len:
                break

            start_pos = index

            while index < text_len and text[index] not in " ,.!?:-\n'\")({}":
                index += 1

            if index >= text_len:
                break

            ret_val.append({"start_pos" : start_pos, "end_pos": index, "sentence": sentence_count})

            if index < text_len and text[index] in ".?!":
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
    global IRREGULARS
    global HELPERS

    if IRREGULARS is None:
        json_data = load_json("passive_voice.json")
        IRREGULARS = json_data["irregulars"]
        HELPERS = json_data["helpers"]

    textData = TextData(text)
    word_count = textData.get_word_count()
    index = 1
    ret_values = []

    while index < word_count:
        word = textData.get_word(index)

        if word is None:
            break

        if (word.endswith("ed") or word in IRREGULARS) and textData.get_word(index - 1) in HELPERS:
            prev_word_data = textData.word_values[index - 1]
            word_data = textData.word_values[index]
            ret_values.append({"start_pos": prev_word_data["start_pos"], "end_pos": word_data["end_pos"], "remark": None})
        index += 1

    return {"findings": ret_values, "score": (len(ret_values)/textData.get_sentence_count())*100}

def check_wordiness(text):
    """Checks the given text for wordiness in accordance to grammark

    Return:
    {
        "score": <score>,
        "findings": [{ "start_pos": <index>, "end_pos": <index>, "remark" : <remark/correction/None> }]
    }

    start_pos: is the start position of the problematic fragment
    end_pos: is the end position of the problematic fragment
    remark: can be a remark, a proposed correction or None if there is no such thing
    """
    global WORDINESS_WORDS

    if WORDINESS_WORDS is None:
        json_data = load_json("wordiness.json")
        WORDINESS_WORDS = json_data["keywords"]

    textData = TextData(text)

    ret_values = []

    for word in WORDINESS_WORDS:
        res = textData.find_substring(word[0])

        for r in res:
            ret_values.append({"start_pos": r["start_pos"], "end_pos": r["end_pos"], "remark": word[1]})

    return {"findings": ret_values, "score": (len(ret_values)/textData.get_sentence_count())*100}

def check_nominalizations(text):
    """Checks the given text for nominalizations in accordance to grammark

    Return:
    {
        "score": <score>,
        "findings": [{ "start_pos": <index>, "end_pos": <index>, "remark" : <remark/correction/None> }]
    }

    start_pos: is the start position of the problematic fragment
    end_pos: is the end position of the problematic fragment
    remark: can be a remark, a proposed correction or None if there is no such thing
    """
    global NOMINALIZATION_POSTFIXES

    if NOMINALIZATION_POSTFIXES is None:
        json_data = load_json("nominalizations.json")
        NOMINALIZATION_POSTFIXES = json_data["postfixes"]

    textData = TextData(text)

    word_count = textData.get_word_count()
    index = 0
    ret_values = []

    while index < word_count:
        word = textData.get_word(index)

        if word is None:
            break

        if len(word) > 7:
            for postfix in NOMINALIZATION_POSTFIXES:
                if word.endswith(postfix):
                    word_data = textData.word_values[index]
                    ret_values.append({"start_pos": word_data["start_pos"], "end_pos": word_data["end_pos"], "remark": None})
        index += 1


    return {"findings": ret_values, "score": (len(ret_values)/word_count)*100}

def check_sentences(text):
    """Checks the given text for sentences in accordance to grammark

    Return:
    {
        "score": <score>,
        "findings": [{ "start_pos": <index>, "end_pos": <index>, "remark" : <remark/correction/None> }]
    }

    start_pos: is the start position of the problematic fragment
    end_pos: is the end position of the problematic fragment
    remark: can be a remark, a proposed correction or None if there is no such thing
    """
    global SENTENCES_STARTS

    if SENTENCES_STARTS is None:
        json_data = load_json("sentences.json")
        SENTENCES_STARTS = json_data["keywords"]

    textData = TextData(text)

    word_count = textData.get_word_count()
    index = 0
    ret_values = []
    sentence_word_count = 0
    current_sentence = -1
    sentence_start = -1

    sentence_considered = []

    while index < word_count:
        word = textData.get_word(index)
        word_data = textData.word_values[index]

        if word is None:
            break

        if current_sentence != word_data["sentence"]:
            current_sentence = word_data["sentence"]
            sentence_word_count = 0
            sentence_start = word_data["start_pos"]

            if word in SENTENCES_STARTS:
                ret_values.append({"start_pos": sentence_start, "end_pos": word_data["end_pos"], "remark": "Sentence starts with And, But, Or"})

        else:
            sentence_word_count += 1

        if sentence_word_count > 50 and current_sentence not in sentence_considered:
            sentence_considered.append(current_sentence)
            ret_values.append({"start_pos": sentence_start, "end_pos": word_data["end_pos"], "remark": "Sentence to large."})
        index += 1

    return {"findings": ret_values, "score": (len(ret_values)/textData.get_sentence_count())*100}

def check_transitions(text):
    """Checks the given text for transitions in accordance to grammark

    Return:
    {
        "score": <score>,
        "findings": [{ "start_pos": <index>, "end_pos": <index>, "remark" : <remark/correction/None> }]
    }

    start_pos: is the start position of the problematic fragment
    end_pos: is the end position of the problematic fragment
    remark: can be a remark, a proposed correction or None if there is no such thing
    """
    global TRANSITIONS

    if TRANSITIONS is None:
        json_data = load_json("transitions.json")
        TRANSITIONS = json_data["keywords"]

    textData = TextData(text)

    ret_values = []

    for word in TRANSITIONS:
        res = textData.find_substring(word)

        for r in res:
            ret_values.append({"start_pos": r["start_pos"], "end_pos": r["end_pos"], "remark": None})

    return {"findings": ret_values, "score": (len(ret_values)/textData.get_sentence_count())*100}

def check_academic(text):
    """Checks the given text for transitions in accordance to grammark

    Return:
    {
        "score": <score>,
        "findings": [{ "start_pos": <index>, "end_pos": <index>, "remark" : <remark/correction/None> }]
    }

    start_pos: is the start position of the problematic fragment
    end_pos: is the end position of the problematic fragment
    remark: can be a remark, a proposed correction or None if there is no such thing
    """
    global ACADEMIC

    if ACADEMIC is None:
        json_data = load_json("academic.json")
        ACADEMIC = json_data["keywords"]

    textData = TextData(text)

    ret_values = []

    for word in ACADEMIC:
        res = textData.find_substring(word[0])

        for r in res:
            ret_values.append({"start_pos": r["start_pos"], "end_pos": r["end_pos"], "remark": word[1]})

    return {"findings": ret_values, "score": (len(ret_values)/textData.get_word_count())*100}

def check_grammar(text):
    """Checks the given text for grammar in accordance to grammark

    Return:
    {
        "score": <score>,
        "findings": [{ "start_pos": <index>, "end_pos": <index>, "remark" : <remark/correction/None> }]
    }

    start_pos: is the start position of the problematic fragment
    end_pos: is the end position of the problematic fragment
    remark: can be a remark, a proposed correction or None if there is no such thing
    """
    global GRAMMAR

    if GRAMMAR is None:
        json_data = load_json("grammar.json")
        GRAMMAR = json_data["keywords"]

    textData = TextData(text)

    ret_values = []

    for word in GRAMMAR:
        res = textData.find_substring(word[0])

        for r in res:
            ret_values.append({"start_pos": r["start_pos"], "end_pos": r["end_pos"], "remark": word[1]})

    return {"findings": ret_values, "score": len(ret_values)}

def check_eggcorns(text):
    """Checks the given text for eggcorns in accordance to grammark

    Return:
    {
        "score": <score>,
        "findings": [{ "start_pos": <index>, "end_pos": <index>, "remark" : <remark/correction/None> }]
    }

    start_pos: is the start position of the problematic fragment
    end_pos: is the end position of the problematic fragment
    remark: can be a remark, a proposed correction or None if there is no such thing
    """
    global EGGCORNS

    if EGGCORNS is None:
        json_data = load_json("eggcorns.json")
        EGGCORNS = json_data["keywords"]

    textData = TextData(text)

    ret_values = []

    for word in EGGCORNS:
        res = textData.find_substring(word[0])

        for r in res:
            ret_values.append({"start_pos": r["start_pos"], "end_pos": r["end_pos"], "remark": word[1]})

    return {"findings": ret_values, "score": len(ret_values)}
