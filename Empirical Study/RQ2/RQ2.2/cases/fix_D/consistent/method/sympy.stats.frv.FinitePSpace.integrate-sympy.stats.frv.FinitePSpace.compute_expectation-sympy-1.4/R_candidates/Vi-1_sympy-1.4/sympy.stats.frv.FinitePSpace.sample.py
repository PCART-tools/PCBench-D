    def sample(self):
        """
        Internal sample method

        Returns dictionary mapping RandomSymbol to realization value.
        """
        expr = Tuple(*self.values)
        cdf = self.sorted_cdf(expr, python_float=True)

        x = random.uniform(0, 1)
        # Find first occurrence with cumulative probability less than x
        # This should be replaced with binary search
        for value, cum_prob in cdf:
            if x < cum_prob:
                # return dictionary mapping RandomSymbols to values
                return dict(list(zip(expr, value)))

        assert False, "We should never have gotten to this point"
