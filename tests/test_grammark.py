import unittest
import sys
sys.path.insert(0, './src/')
from grammark import TextData

testText = "In this paper we discussed stochastic simulation to support the design process of distributed ledger applications. We discussed a general approach, that is customizable to specific use cases and evaluated it on the use case of German waterway transportation. Despite our initial expectation, transaction throughput and the unreasonable growth in ledger size have not proven to be the limiting factors when using public ledgers. In fact, stochastic simulation unveiled, that it is technically up to the task. Although, the expected transaction fees, that are strongly affected by speculative price developments object the use of public ledgers."

class TestGrammark(unittest.TestCase):

    def test_lexer(self):
        textData = TextData(testText)
        print(textData.word_values)
        self.assertFalse(True)
