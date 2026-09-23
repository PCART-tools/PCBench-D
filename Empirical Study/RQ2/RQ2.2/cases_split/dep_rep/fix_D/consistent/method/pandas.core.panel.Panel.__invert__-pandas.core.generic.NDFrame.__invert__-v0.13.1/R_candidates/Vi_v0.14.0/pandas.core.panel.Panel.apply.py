    def apply(self, func, axis='major', **kwargs):
        """
        Applies function along input axis of the Panel

        Parameters
        ----------
        func : function
            Function to apply to each combination of 'other' axes
            e.g. if axis = 'items', then the combination of major_axis/minor_axis
            will be passed a Series
        axis : {'major', 'minor', 'items'}
        Additional keyword arguments will be passed as keywords to the function

        Examples
        --------
        >>> p.apply(numpy.sqrt) # returns a Panel
        >>> p.apply(lambda x: x.sum(), axis=0) # equiv to p.sum(0)
        >>> p.apply(lambda x: x.sum(), axis=1) # equiv to p.sum(1)
        >>> p.apply(lambda x: x.sum(), axis=2) # equiv to p.sum(2)

        Returns
        -------
        result : Pandas Object
        """

        if kwargs and not isinstance(func, np.ufunc):
            f = lambda x: func(x, **kwargs)
        else:
            f = func

        # 2d-slabs
        if isinstance(axis, (tuple,list)) and len(axis) == 2:
            return self._apply_2d(f, axis=axis)

        axis = self._get_axis_number(axis)

        # try ufunc like
        if isinstance(f, np.ufunc):
            try:
                result = np.apply_along_axis(func, axis, self.values)
                return self._wrap_result(result, axis=axis)
            except (AttributeError):
                pass

        # 1d
        return self._apply_1d(f, axis=axis)
