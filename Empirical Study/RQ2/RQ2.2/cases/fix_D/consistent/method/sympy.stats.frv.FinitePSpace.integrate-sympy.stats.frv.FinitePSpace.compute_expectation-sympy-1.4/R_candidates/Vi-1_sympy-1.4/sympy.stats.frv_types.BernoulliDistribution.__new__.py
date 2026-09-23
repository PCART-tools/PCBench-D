    def __new__(cls, *args):
        p = args[BernoulliDistribution._argnames.index('p')]
        p_sym = sympify(p)

        if fuzzy_not(fuzzy_and((p_sym.is_nonnegative, (p_sym - 1).is_nonpositive))):
            raise ValueError("p = %s is not in range [0, 1]." % str(p))
        else:
            return super(BernoulliDistribution, cls).__new__(cls, *args)
