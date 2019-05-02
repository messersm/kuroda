from unittest import TestCase

from kuroda.automata import DFA, collect


DELTA = {
    (0, 'a'): 1,
    (0, 'b'): 0,
    (1, 'a'): 1,
    (1, 'b'): 2,
    (2, 'a'): 0,
    (2, 'b'): 0
}

DFA_RUNS = {
    "abbaa" : [
        ("", 0, "abbaa"),
        ("a", 1, "bbaa"),
        ("ab", 2, "baa"),
        ("abb", 0, "aa"),
        ("abba", 1, "a"),
        ("abbaa", 1, "")
    ]
}

class ToolTests(TestCase):
    def test_collect(self):
        Q, Sigma = collect(DELTA)
        self.assertEqual(Q, {0, 1, 2})
        self.assertEqual(Sigma, {'a', 'b'})


class DFATests(TestCase):
    def test_invalid_q0(self):
        self.assertRaises(ValueError, DFA, Q={1, 2, 3}, q0=4)

    def test_default_Q(self):
        M = DFA(delta=DELTA)
        self.assertEqual(M.Q, {0, 1, 2})

    def test_invalid_Q(self):
        self.assertRaises(ValueError, DFA, Q={2, 3, 4}, delta=DELTA)

    def test_default_Sigma(self):
        M = DFA(delta=DELTA)
        self.assertEqual(M.Sigma, {'a', 'b'})

    def test_invalid_Sigma(self):
        self.assertRaises(ValueError, DFA, Sigma={'b', 'c'}, delta=DELTA)

    def test_runs(self):
        M = DFA(delta=DELTA)

        for word in DFA_RUNS:
            M.reset(word)

            length = len(DFA_RUNS[word])
            for count, config in enumerate(DFA_RUNS[word]):
                self.assertEqual(config, M.config)
                if count < length - 1:
                    M.step()

            # make sure, the next step() raises StopIteration
            self.assertRaises(StopIteration, M.step)
