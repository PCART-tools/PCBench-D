    @classmethod
    def _add_logical_methods(cls):
        """ add in logical methods """

        _doc = """

        %(desc)s

        Parameters
        ----------
        All arguments to numpy.%(outname)s are accepted.

        Returns
        -------
        %(outname)s : bool or array_like (if axis is specified)
            A single element array_like may be converted to bool."""

        def _make_logical_function(name, desc, f):
            @Substitution(outname=name, desc=desc)
            @Appender(_doc)
            def logical_func(self, *args, **kwargs):
                result = f(self.values)
                if (isinstance(result, (np.ndarray, ABCSeries, Index)) and
                        result.ndim == 0):
                    # return NumPy type
                    return result.dtype.type(result.item())
                else:  # pragma: no cover
                    return result

            logical_func.__name__ = name
            return logical_func

        cls.all = _make_logical_function('all', 'Return whether all elements '
                                                'are True',
                                         np.all)
        cls.any = _make_logical_function('any',
                                         'Return whether any element is True',
                                         np.any)
