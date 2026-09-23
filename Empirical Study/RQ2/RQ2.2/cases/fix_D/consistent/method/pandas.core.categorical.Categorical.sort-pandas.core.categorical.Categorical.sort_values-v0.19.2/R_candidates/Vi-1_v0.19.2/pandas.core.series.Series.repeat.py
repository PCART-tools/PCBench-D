    def repeat(self, reps, *args, **kwargs):
        """
        Repeat elements of an Series. Refer to `numpy.ndarray.repeat`
        for more information about the `reps` argument.

        See also
        --------
        numpy.ndarray.repeat
        """
        nv.validate_repeat(args, kwargs)
        new_index = self.index.repeat(reps)
        new_values = self._values.repeat(reps)
        return self._constructor(new_values,
                                 index=new_index).__finalize__(self)
