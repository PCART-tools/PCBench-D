    def repeat(self, reps):
        """
        See ndarray.repeat
        """
        new_index = self.index.repeat(reps)
        new_values = self.values.repeat(reps)
        return self._constructor(new_values,
                                 index=new_index).__finalize__(self)
