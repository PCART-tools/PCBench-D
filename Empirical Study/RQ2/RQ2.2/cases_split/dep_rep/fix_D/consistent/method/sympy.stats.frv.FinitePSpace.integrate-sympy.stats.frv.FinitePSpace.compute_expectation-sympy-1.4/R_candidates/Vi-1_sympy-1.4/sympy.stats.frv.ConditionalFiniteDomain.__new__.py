    def __new__(cls, domain, condition):
        """
        Create a new instance of ConditionalFiniteDomain class
        """
        if condition is True:
            return domain
        cond = rv_subs(condition)
        # Check that we aren't passed a condition like die1 == z
        # where 'z' is a symbol that we don't know about
        # We will never be able to test this equality through iteration
        if not cond.free_symbols.issubset(domain.free_symbols):
            raise ValueError('Condition "%s" contains foreign symbols \n%s.\n' % (
                condition, tuple(cond.free_symbols - domain.free_symbols)) +
                "Will be unable to iterate using this condition")

        return Basic.__new__(cls, domain, cond)
