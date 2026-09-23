    @deprecate_kwarg(old_arg_name='raise_on_error', new_arg_name='errors',
                     mapping={True: 'raise', False: 'ignore'})
    def astype(self, dtype, copy=True, errors='raise', **kwargs):
        """
        Cast object to input numpy.dtype
        Return a copy when copy = True (be really careful with this!)

        Parameters
        ----------
        dtype : data type, or dict of column name -> data type
            Use a numpy.dtype or Python type to cast entire pandas object to
            the same type. Alternatively, use {col: dtype, ...}, where col is a
            column label and dtype is a numpy.dtype or Python type to cast one
            or more of the DataFrame's columns to column-specific types.
        errors : {'raise', 'ignore'}, default 'raise'.
            Control raising of exceptions on invalid data for provided dtype.

            - ``raise`` : allow exceptions to be raised
            - ``ignore`` : suppress exceptions. On error return original object

            .. versionadded:: 0.20.0

        raise_on_error : DEPRECATED use ``errors`` instead
        kwargs : keyword arguments to pass on to the constructor

        Returns
        -------
        casted : type of caller
        """
        if isinstance(dtype, collections.Mapping):
            if self.ndim == 1:  # i.e. Series
                if len(dtype) > 1 or list(dtype.keys())[0] != self.name:
                    raise KeyError('Only the Series name can be used for '
                                   'the key in Series dtype mappings.')
                new_type = list(dtype.values())[0]
                return self.astype(new_type, copy, errors, **kwargs)
            elif self.ndim > 2:
                raise NotImplementedError(
                    'astype() only accepts a dtype arg of type dict when '
                    'invoked on Series and DataFrames. A single dtype must be '
                    'specified when invoked on a Panel.'
                )
            for col_name in dtype.keys():
                if col_name not in self:
                    raise KeyError('Only a column name can be used for the '
                                   'key in a dtype mappings argument.')
            from pandas import concat
            results = []
            for col_name, col in self.iteritems():
                if col_name in dtype:
                    results.append(col.astype(dtype[col_name], copy=copy))
                else:
                    results.append(results.append(col.copy() if copy else col))
            return concat(results, axis=1, copy=False)

        # else, only a single dtype is given
        new_data = self._data.astype(dtype=dtype, copy=copy, errors=errors,
                                     **kwargs)
        return self._constructor(new_data).__finalize__(self)
