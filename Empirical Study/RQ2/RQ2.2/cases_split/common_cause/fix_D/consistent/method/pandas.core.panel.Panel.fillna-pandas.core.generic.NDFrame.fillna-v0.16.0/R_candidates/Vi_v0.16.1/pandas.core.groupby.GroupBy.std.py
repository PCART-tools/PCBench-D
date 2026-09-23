    def std(self, ddof=1):
        """
        Compute standard deviation of groups, excluding missing values

        For multiple groupings, the result index will be a MultiIndex
        """
        # todo, implement at cython level?
        return np.sqrt(self.var(ddof=ddof))
