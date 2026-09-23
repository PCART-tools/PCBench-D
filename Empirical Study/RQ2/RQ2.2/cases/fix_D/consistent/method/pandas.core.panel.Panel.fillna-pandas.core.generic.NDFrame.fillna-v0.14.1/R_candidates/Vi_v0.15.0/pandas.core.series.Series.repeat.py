    def repeat(self, reps):
        """
        return a new Series with the values repeated reps times

        See also
        --------
        numpy.ndarray.repeat
        """
        new_index = self.index.repeat(reps)
        new_values = self.values.repeat(reps)
        return self._constructor(new_values,
                                 index=new_index).__finalize__(self)
