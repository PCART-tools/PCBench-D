    def apply(self, func, axis='major', **kwargs):
        """
        Applies function along axis (or axes) of the Panel

        Parameters
        ----------
        func : function
            Function to apply to each combination of 'other' axes
            e.g. if axis = 'items', the combination of major_axis/minor_axis
            will each be passed as a Series; if axis = ('items', 'major'),
            DataFrames of items & major axis will be passed
        axis : {'items', 'minor', 'major'}, or {0, 1, 2}, or a tuple with two
            axes
        Additional keyword arguments will be passed as keywords to the function

        Examples
        --------

        Returns a Panel with the square root of each element

        >>> p = pd.Panel(np.random.rand(4,3,2))
        >>> p.apply(np.sqrt)

        Equivalent to p.sum(1), returning a DataFrame

        >>> p.apply(lambda x: x.sum(), axis=1)

        Equivalent to previous:

        >>> p.apply(lambda x: x.sum(), axis='minor')

        Return the shapes of each DataFrame over axis 2 (i.e the shapes of
        items x major), as a Series

        >>> p.apply(lambda x: x.shape, axis=(0,1))

        Returns
        -------
        result : Panel, DataFrame, or Series
        """

        if kwargs and not isinstance(func, np.ufunc):
            f = lambda x: func(x, **kwargs)
        else:
            f = func

        # 2d-slabs
        if isinstance(axis, (tuple, list)) and len(axis) == 2:
            return self._apply_2d(f, axis=axis)

        axis = self._get_axis_number(axis)

        # try ufunc like
        if isinstance(f, np.ufunc):
            try:
                with np.errstate(all='ignore'):
                    result = np.apply_along_axis(func, axis, self.values)
                return self._wrap_result(result, axis=axis)
            except (AttributeError):
                pass

        # 1d
        return self._apply_1d(f, axis=axis)
