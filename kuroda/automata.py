from itertools import product

class DFA(object):
    """Implements a deterministic finite automaton (DFA/DFSM/DFSA).
    """
    def __init__(self, Q=None, Sigma=None, delta=None, q0=0, F=frozenset()):
        """Create a new DFA given

        Args:
            Q (iterable): A set of states.
            Sigma (iterable): The input alphabet.
            delta (dict): The transition function as mapping (q, a) -> q'
                          where q, q' are in Q and a is in Sigma.
            q0: The start state (must be in Q).
            F(iterable): A set of accepting states (must be subset of Q).

        Q and Sigma will be automatically derived from delta, if not given.
        """

        if delta is None:
            self.delta = dict()
        else:
            self.delta = dict(delta)

        collected_Q, collected_Sigma = collect(self.delta)

        if Q is None:
            self.Q = frozenset(collected_Q)
        else:
            self.Q = frozenset(Q)

        if Sigma is None:
            self.Sigma = frozenset(collected_Sigma)
        else:
            self.Sigma = frozenset(Sigma)

        self.F = frozenset(F)
        self.delta = delta
        self.q0 = q0

        # some sanity checks
        if not collected_Q.issubset(self.Q):
            raise ValueError("delta references states, which are not in Q.")

        if not collected_Sigma.issubset(self.Sigma):
            raise ValueError("delta references symbols, which are not in Sigma.")

        if not self.F.issubset(self.Q):
            raise ValueError("F is not a subset of Q.")

        if self.q0 not in self.Q:
            raise ValueError("q0 is not in Q.")

        # input word and position within the word and the current state
        self.__w = None
        self.__pos = 0
        self.__q = self.q0

    def reset(self, word):
        """Reset the automaton and set the given word as input."""

        for symbol in word:
            if symbol not in self.Sigma:
                raise ValueError(
                    "Invalid input symbol '%s' (not in Sigma)." % symbol)

        self.__q = self.q0
        self.__w = str(word)
        self.__pos = 0

    @property
    def config(self):
        return self.__w[:self.__pos], self.__q, self.__w[self.__pos:]

    def step(self):
        try:
            symbol = self.__w[self.__pos]
        except IndexError:
            raise StopIteration()
        except TypeError:
            raise TypeError("Invalid input word: %s" % self.__w)

        try:
            next_q = self.delta[(self.__q, symbol)]
        except KeyError:
            raise RuntimeError(
                "No transition given for (%s, %s)" % (self.__q, symbol))

        self.__q = next_q
        self.__pos += 1

    def accepts(self, word):
        self.reset(word)

        while True:
            try:
                self.step()
            except StopIteration:
                return self.__q in self.F


def collect(delta):
    """Return the states and alphabet used in the transition function delta."""

    Q = set()
    Sigma = set()

    for (q, a), r in delta.items():
        Q.add(q)
        Q.add(r)
        Sigma.add(a)

    return Q, Sigma


def L(M):
    """Return an iterator over the language of the given machine M.
    """
    length = 0
    while True:
        for word in product(M.Sigma, length):
            if M.accepts(word):
                yield word
        length += 1
