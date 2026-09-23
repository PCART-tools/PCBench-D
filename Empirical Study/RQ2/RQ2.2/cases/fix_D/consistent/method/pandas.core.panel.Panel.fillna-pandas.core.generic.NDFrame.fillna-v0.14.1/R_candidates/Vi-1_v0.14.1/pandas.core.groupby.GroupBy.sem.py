    def sem(self, ddof=1):
        """
        Compute standard error of the mean of groups, excluding missing values

        For multiple groupings, the result index will be a MultiIndex
        """
        return self.std(ddof=ddof)/np.sqrt(self.count())
