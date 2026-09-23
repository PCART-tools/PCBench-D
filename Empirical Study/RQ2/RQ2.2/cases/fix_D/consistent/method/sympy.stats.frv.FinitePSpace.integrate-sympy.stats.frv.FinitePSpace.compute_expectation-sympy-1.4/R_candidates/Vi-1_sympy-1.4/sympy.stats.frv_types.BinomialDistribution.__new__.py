    def __new__(cls, *args):
        n = args[BinomialDistribution._argnames.index('n')]
        p = args[BinomialDistribution._argnames.index('p')]
        n_sym = sympify(n)
        p_sym = sympify(p)

        if fuzzy_not(fuzzy_and((n_sym.is_integer, n_sym.is_nonnegative))):
            raise ValueError("'n' must be positive integer. n = %s." % str(n))
        elif fuzzy_not(fuzzy_and((p_sym.is_nonnegative, (p_sym - 1).is_nonpositive))):
            raise ValueError("'p' must be: 0 <= p <= 1 . p = %s" % str(p))
        else:
            return super(BinomialDistribution, cls).__new__(cls, *args)
