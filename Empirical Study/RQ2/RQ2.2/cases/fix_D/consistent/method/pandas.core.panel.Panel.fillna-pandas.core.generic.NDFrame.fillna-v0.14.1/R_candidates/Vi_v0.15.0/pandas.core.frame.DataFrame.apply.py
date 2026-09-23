    def apply(self, func, axis=0, broadcast=False, raw=False, reduce=None,
              args=(), **kwds):
        """
        Applies function along input axis of DataFrame.

        Objects passed to functions are Series objects having index
        either the DataFrame's index (axis=0) or the columns (axis=1).
        Return type depends on whether passed function aggregates, or the
        reduce argument if the DataFrame is empty.

        Parameters
        ----------
        func : function
            Function to apply to each column/row
        axis : {0, 1}
            * 0 : apply function to each column
            * 1 : apply function to each row
        broadcast : boolean, default False
            For aggregation functions, return object of same size with values
            propagated
        reduce : boolean or None, default None
            Try to apply reduction procedures. If the DataFrame is empty,
            apply will use reduce to determine whether the result should be a
            Series or a DataFrame. If reduce is None (the default), apply's
            return value will be guessed by calling func an empty Series (note:
            while guessing, exceptions raised by func will be ignored). If
            reduce is True a Series will always be returned, and if False a
            DataFrame will always be returned.
        raw : boolean, default False
            If False, convert each row or column into a Series. If raw=True the
            passed function will receive ndarray objects instead. If you are
            just applying a NumPy reduction function this will achieve much
            better performance
        args : tuple
            Positional arguments to pass to function in addition to the
            array/series
        Additional keyword arguments will be passed as keywords to the function

        Notes
        -----
        In the current implementation apply calls func twice on the
        first column/row to decide whether it can take a fast or slow
        code path. This can lead to unexpected behavior if func has
        side-effects, as they will take effect twice for the first
        column/row.

        Examples
        --------
        >>> df.apply(numpy.sqrt) # returns DataFrame
        >>> df.apply(numpy.sum, axis=0) # equiv to df.sum(0)
        >>> df.apply(numpy.sum, axis=1) # equiv to df.sum(1)

        See also
        --------
        DataFrame.applymap: For elementwise operations

        Returns
        -------
        applied : Series or DataFrame
        """
        axis = self._get_axis_number(axis)
        if kwds or args and not isinstance(func, np.ufunc):
            f = lambda x: func(x, *args, **kwds)
        else:
            f = func

        if len(self.columns) == 0 and len(self.index) == 0:
            return self._apply_empty_result(func, axis, reduce, *args, **kwds)

        if isinstance(f, np.ufunc):
            results = f(self.values)
            return self._constructor(data=results, index=self.index,
                                     columns=self.columns, copy=False)
        else:
            if not broadcast:
                if not all(self.shape):
                    return self._apply_empty_result(func, axis, reduce, *args,
                                                    **kwds)

                if raw and not self._is_mixed_type:
                    return self._apply_raw(f, axis)
                else:
                    if reduce is None:
                        reduce = True
                    return self._apply_standard(f, axis, reduce=reduce)
            else:
                return self._apply_broadcast(f, axis)
