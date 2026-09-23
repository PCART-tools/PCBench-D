    def reset_index(self, level=None, drop=False, name=None, inplace=False):
        """
        Analogous to the :meth:`pandas.DataFrame.reset_index` function, see
        docstring there.

        Parameters
        ----------
        level : int, str, tuple, or list, default None
            Only remove the given levels from the index. Removes all levels by
            default
        drop : boolean, default False
            Do not try to insert index into dataframe columns
        name : object, default None
            The name of the column corresponding to the Series values
        inplace : boolean, default False
            Modify the Series in place (do not create a new object)

        Returns
        ----------
        resetted : DataFrame, or Series if drop == True

        Examples
        --------
        >>> s = pd.Series([1, 2, 3, 4], index=pd.Index(['a', 'b', 'c', 'd'],
        ...                                            name = 'idx'))
        >>> s.reset_index()
           index  0
        0      0  1
        1      1  2
        2      2  3
        3      3  4

        >>> arrays = [np.array(['bar', 'bar', 'baz', 'baz', 'foo',
        ...                     'foo', 'qux', 'qux']),
        ...           np.array(['one', 'two', 'one', 'two', 'one', 'two',
        ...                     'one', 'two'])]
        >>> s2 = pd.Series(
        ...     np.random.randn(8),
        ...     index=pd.MultiIndex.from_arrays(arrays,
        ...                                     names=['a', 'b']))
        >>> s2.reset_index(level='a')
               a         0
        b
        one  bar -0.286320
        two  bar -0.587934
        one  baz  0.710491
        two  baz -1.429006
        one  foo  0.790700
        two  foo  0.824863
        one  qux -0.718963
        two  qux -0.055028
        """
        inplace = validate_bool_kwarg(inplace, 'inplace')
        if drop:
            new_index = _default_index(len(self))
            if level is not None and isinstance(self.index, MultiIndex):
                if not isinstance(level, (tuple, list)):
                    level = [level]
                level = [self.index._get_level_number(lev) for lev in level]
                if len(level) < len(self.index.levels):
                    new_index = self.index.droplevel(level)

            if inplace:
                self.index = new_index
                # set name if it was passed, otherwise, keep the previous name
                self.name = name or self.name
            else:
                return self._constructor(self._values.copy(),
                                         index=new_index).__finalize__(self)
        elif inplace:
            raise TypeError('Cannot reset_index inplace on a Series '
                            'to create a DataFrame')
        else:
            df = self.to_frame(name)
            return df.reset_index(level=level, drop=drop)
