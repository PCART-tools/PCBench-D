    @deprecate_kwarg(old_arg_name='reps', new_arg_name='repeats')
    def repeat(self, repeats, *args, **kwargs):
        """
        Repeat elements of an Series. Refer to `numpy.ndarray.repeat`
        for more information about the `repeats` argument.

        See also
        --------
        numpy.ndarray.repeat
        """
        nv.validate_repeat(args, kwargs)
        new_index = self.index.repeat(repeats)
        new_values = self._values.repeat(repeats)
        return self._constructor(new_values,
                                 index=new_index).__finalize__(self)
