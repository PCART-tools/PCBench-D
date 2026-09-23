    def xs(self, key, axis=0, level=None, copy=True, drop_level=True):
        """
        Returns a cross-section (row(s) or column(s)) from the DataFrame.
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
        copy : boolean, default True
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
        >>> s = df.xs('a', copy=False)
        >>> s['A'] = 100
        >>> df
             A  B  C
        a  100  5  2
        b    4  0  9
        c    9  7  3


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

        """
        axis = self._get_axis_number(axis)
        labels = self._get_axis(axis)
        if level is not None:
            loc, new_ax = labels.get_loc_level(key, level=level,
                                               drop_level=drop_level)

            if not copy and not isinstance(loc, slice):
                raise ValueError('Cannot retrieve view (copy=False)')

            # level = 0
            loc_is_slice = isinstance(loc, slice)
            if not loc_is_slice:
                indexer = [slice(None)] * 2
                indexer[axis] = loc
                indexer = tuple(indexer)
            else:
                indexer = loc
                lev_num = labels._get_level_number(level)
                if labels.levels[lev_num].inferred_type == 'integer':
                    indexer = self.index[loc]

            # select on the correct axis
            if axis == 1 and loc_is_slice:
                indexer = slice(None), indexer
            result = self.ix[indexer]
            setattr(result, result._get_axis_name(axis), new_ax)
            return result

        if axis == 1:
            data = self[key]
            if copy:
                data = data.copy()
            return data

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

            new_values, copy = self._data.fast_2d_xs(loc, copy=copy)
            result = Series(new_values, index=self.columns,
                            name=self.index[loc])
            result.is_copy=True

        else:
            result = self[loc]
            result.index = new_index

        return result
