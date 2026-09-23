    def apply(self, func, axis=0, broadcast=False, raw=False, reduce=True,
              args=(), **kwds):
        """
        Applies function along input axis of DataFrame.

        Objects passed to functions are Series objects having index
        either the DataFrame's index (axis=0) or the columns (axis=1).
        Return type depends on whether passed function aggregates

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
        reduce : boolean, default True
            Try to apply reduction procedures
        raw : boolean, default False
            If False, convert each row or column into a Series. If raw=True the
            passed function will receive ndarray objects instead. If you are
            just applying a NumPy reduction function this will achieve much
            better performance
        args : tuple
            Positional arguments to pass to function in addition to the
            array/series
        Additional keyword arguments will be passed as keywords to the function

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
        if len(self.columns) == 0 and len(self.index) == 0:
            return self

        axis = self._get_axis_number(axis)
        if kwds or args and not isinstance(func, np.ufunc):
            f = lambda x: func(x, *args, **kwds)
        else:
            f = func

        if isinstance(f, np.ufunc):
            results = f(self.values)
            return self._constructor(data=results, index=self.index,
                                     columns=self.columns, copy=False)
        else:
            if not broadcast:
                if not all(self.shape):
                    # How to determine this better?
                    is_reduction = False
                    try:
                        is_reduction = not isinstance(f(_EMPTY_SERIES), Series)
                    except Exception:
                        pass

                    if is_reduction:
                        return Series(NA, index=self._get_agg_axis(axis))
                    else:
                        return self.copy()

                if raw and not self._is_mixed_type:
                    return self._apply_raw(f, axis)
                else:
                    return self._apply_standard(f, axis, reduce=reduce)
            else:
                return self._apply_broadcast(f, axis)
