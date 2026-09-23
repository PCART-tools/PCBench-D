    def abs(self):
        """
        Return an object with absolute value taken. Only applicable to objects
        that are all numeric

        Returns
        -------
        abs: type of caller
        """
        return self._constructor(np.abs(self.values),
                                 index=self.index).__finalize__(self)
