    @deprecate_kwarg(old_arg_name='n', new_arg_name='repeats')
    def repeat(self, repeats, *args, **kwargs):
        """
        Repeat elements of an Index. Refer to `numpy.ndarray.repeat`
        for more information about the `repeats` argument.

        See also
        --------
        numpy.ndarray.repeat
        """
        nv.validate_repeat(args, kwargs)
        return self._shallow_copy(self._values.repeat(repeats))
