    def xs(self, key, axis=0, level=None, copy=None, drop_level=True):
        """
        Returns a cross-section (row(s) or column(s)) from the Series/DataFrame.
        Defaults to cross-section on the rows (axis=0).

        Parameters
        ----------
        key : object
            Some label contained in the index, or partially in a MultiIndex
        axis : int, default 0
            Axis to retrieve cross-section on
        level : object, defaults to first n levels (n=1 or len(key))
            In case of a key partially contained in a MultiIndex, indicate
            which levels are used. Levels can be referred by label or position.
        copy : boolean [deprecated]
            Whether to make a copy of the data
        drop_level : boolean, default True
            If False, returns object with same levels as self.

        Examples
        --------
        >>> df
           A  B  C
        a  4  5  2
        b  4  0  9
        c  9  7  3
        >>> df.xs('a')
        A    4
        B    5
        C    2
        Name: a
        >>> df.xs('C', axis=1)
        a    2
        b    9
        c    3
        Name: C

        >>> df
                            A  B  C  D
        first second third
        bar   one    1      4  1  8  9
              two    1      7  5  5  0
        baz   one    1      6  6  8  0
              three  2      5  3  5  3
        >>> df.xs(('baz', 'three'))
               A  B  C  D
        third
        2      5  3  5  3
        >>> df.xs('one', level=1)
                     A  B  C  D
        first third
        bar   1      4  1  8  9
        baz   1      6  6  8  0
        >>> df.xs(('baz', 2), level=[0, 'third'])
                A  B  C  D
        second
        three   5  3  5  3

        Returns
        -------
        xs : Series or DataFrame

        Notes
        -----
        xs is only for getting, not setting values.

        MultiIndex Slicers is a generic way to get/set values on any level or levels
        it is a superset of xs functionality, see :ref:`MultiIndex Slicers <advanced.mi_slicers>`

        """
        if copy is not None:
            warnings.warn("copy keyword is deprecated, "
                          "default is to return a copy or a view if possible")

        axis = self._get_axis_number(axis)
        labels = self._get_axis(axis)
        if level is not None:
            loc, new_ax = labels.get_loc_level(key, level=level,
                                               drop_level=drop_level)

            # convert to a label indexer if needed
            if isinstance(loc, slice):
                lev_num = labels._get_level_number(level)
                if labels.levels[lev_num].inferred_type == 'integer':
                    loc = labels[loc]

            # create the tuple of the indexer
            indexer = [slice(None)] * self.ndim
            indexer[axis] = loc
            indexer = tuple(indexer)

            result = self.ix[indexer]
            setattr(result, result._get_axis_name(axis), new_ax)
            return result

        if axis == 1:
            return self[key]

        self._consolidate_inplace()

        index = self.index
        if isinstance(index, MultiIndex):
            loc, new_index = self.index.get_loc_level(key,
                                                      drop_level=drop_level)
        else:
            loc = self.index.get_loc(key)

            if isinstance(loc, np.ndarray):
                if loc.dtype == np.bool_:
                    inds, = loc.nonzero()
                    return self.take(inds, axis=axis, convert=False)
                else:
                    return self.take(loc, axis=axis, convert=True)

            if not np.isscalar(loc):
                new_index = self.index[loc]

        if np.isscalar(loc):
            from pandas import Series
            new_values = self._data.fast_xs(loc)

            # may need to box a datelike-scalar
            #
            # if we encounter an array-like and we only have 1 dim
            # that means that their are list/ndarrays inside the Series!
            # so just return them (GH 6394)
            if not is_list_like(new_values) or self.ndim == 1:
                return _maybe_box_datetimelike(new_values)

            result = Series(new_values,
                            index=self.columns,
                            name=self.index[loc],
                            copy=copy,
                            dtype=new_values.dtype)

        else:
            result = self.iloc[loc]
            result.index = new_index

        # this could be a view
        # but only in a single-dtyped view slicable case
        result._set_is_copy(self, copy=not result._is_view)
        return result
