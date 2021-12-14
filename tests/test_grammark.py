import unittest
import sys
sys.path.insert(0, './src/')
from grammark import TextData, check_wordiness, check_nominalizations, check_passive_voice, check_sentences, check_academic, check_transitions, check_grammar, check_eggcorns

testText = "In this paper we discussed stochastic simulation to support the design process of distributed ledger applications. We discussed a general approach, that is customizable to specific use cases and evaluated it on the use case of German waterway transportation. Despite our initial expectation, transaction throughput and the unreasonable growth in ledger size have not proven to be the limiting factors when using public ledgers. In fact, stochastic simulation unveiled, that it is technically up to the task. Although, the expected transaction fees, that are strongly affected by speculative price developments object the use of public ledgers."

# 97 word sentence from Jose Saramago "blindness"
testText2 = "On offering to help the blind man, the man who then stole his car, had not, at that precise moment, had any evil intention, quite the contrary, what he did was nothing more than obey those feelings of generosity and altruism which, as everyone knows, are the two best traits of human nature and to be found in much more hardened criminals than this one, a simple car-thief without any hope of advancing in his profession, exploited by the real owners of this enterprise, for it is they who take advantage of the needs of the poor."

def printWords(ev, text):
    for e in ev:
        print(text[e["start_pos"]:e["end_pos"]])

class TestGrammark(unittest.TestCase):

    def test_lexer(self):
        textData = TextData(testText)
        self.assertEqual(len(textData.word_values), 96)
        self.assertEqual(textData.get_sentence_count(), 5)

    def test_passive_voice(self):
        text = "The savannah is roamed by beautiful giraffes."
        res = check_passive_voice(text)

        self.assertEqual(res["findings"][0]["start_pos"], 13)
        self.assertEqual(res["findings"][0]["end_pos"], 22)

        self.assertEqual(res["score"], 100)

    def test_wordiness(self):
        res = check_wordiness(testText)

        self.assertEqual(res["findings"][0]["start_pos"], 148)
        self.assertEqual(res["findings"][0]["end_pos"], 155)
        self.assertEqual(res["findings"][0]["remark"], "DELETE when possible")

        self.assertEqual(res["findings"][1]["start_pos"], 549)
        self.assertEqual(res["findings"][1]["end_pos"], 557)
        self.assertEqual(res["findings"][1]["remark"], "DELETE when possible")

        self.assertEqual(res["findings"][2]["start_pos"], 428)
        self.assertEqual(res["findings"][2]["end_pos"], 435)
        self.assertEqual(res["findings"][2]["remark"], "DELETE")

        self.assertEqual(res["score"], 60)

    def test_nominalizations(self):
        res = check_nominalizations(testText)

        self.assertEqual(res["findings"][0]["start_pos"], 38)
        self.assertEqual(res["findings"][0]["end_pos"], 48)

        self.assertEqual(res["findings"][1]["start_pos"], 101)
        self.assertEqual(res["findings"][1]["end_pos"], 113)

        self.assertEqual(res["findings"][2]["start_pos"], 243)
        self.assertEqual(res["findings"][2]["end_pos"], 257)

        self.assertEqual(res["findings"][3]["start_pos"], 279)
        self.assertEqual(res["findings"][3]["end_pos"], 290)

        self.assertEqual(res["findings"][4]["start_pos"], 384)
        self.assertEqual(res["findings"][4]["end_pos"], 392)

        self.assertEqual(res["findings"][5]["start_pos"], 448)
        self.assertEqual(res["findings"][5]["end_pos"], 458)

        self.assertEqual(res["findings"][6]["start_pos"], 597)
        self.assertEqual(res["findings"][6]["end_pos"], 609)

        self.assertEqual(int(res["score"]), 7)

    def test_sentences(self):
        res = check_sentences(testText2)

        self.assertEqual(res["findings"][0]["start_pos"], 0)
        self.assertEqual(res["findings"][0]["end_pos"], 283)
        self.assertEqual(res["findings"][0]["remark"], "Sentence to large.")

        self.assertEqual(int(res["score"]), 100)

    def test_transitions(self):
        res = check_transitions(testText)

        self.assertEqual(res["findings"][0]["start_pos"], 508)
        self.assertEqual(res["findings"][0]["end_pos"], 516)

        self.assertEqual(res["findings"][1]["start_pos"], 259)
        self.assertEqual(res["findings"][1]["end_pos"], 266)

        self.assertEqual(res["findings"][2]["start_pos"], 428)
        self.assertEqual(res["findings"][2]["end_pos"], 435)

        self.assertEqual(res["score"], 60)

    def test_academic(self):
        res = check_academic(testText2)

        self.assertEqual(res["findings"][0]["start_pos"], 15)
        self.assertEqual(res["findings"][0]["end_pos"], 19)
        self.assertEqual(res["findings"][0]["remark"], "assist/ aid")

        self.assertEqual(res["findings"][1]["start_pos"], 30)
        self.assertEqual(res["findings"][1]["end_pos"], 33)
        self.assertEqual(res["findings"][1]["remark"], "male")

        self.assertEqual(res["findings"][2]["start_pos"], 39)
        self.assertEqual(res["findings"][2]["end_pos"], 42)
        self.assertEqual(res["findings"][2]["remark"], "male")

        self.assertEqual(int(res["score"]), 3)

    def test_grammar(self):
        text = "I wreck havoc"
        res = check_grammar(text)

        self.assertEqual(res["findings"][0]["start_pos"], 2)
        self.assertEqual(res["findings"][0]["end_pos"], 13)
        self.assertEqual(res["findings"][0]["remark"], "wreak havoc")

        self.assertEqual(res["score"], 1)

    def test_eggcorns(self):
        text = "I like this expresso"
        res = check_eggcorns(text)

        self.assertEqual(res["findings"][0]["start_pos"], 12)
        self.assertEqual(res["findings"][0]["end_pos"], 20)
        self.assertEqual(res["findings"][0]["remark"], "espresso")

        self.assertEqual(res["score"], 1)
