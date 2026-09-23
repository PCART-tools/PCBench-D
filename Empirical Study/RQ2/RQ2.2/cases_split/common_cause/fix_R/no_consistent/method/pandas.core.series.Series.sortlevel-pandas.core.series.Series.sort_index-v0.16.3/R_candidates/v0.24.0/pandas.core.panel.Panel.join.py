    def join(self, other, how='left', lsuffix='', rsuffix=''):
        """
        Join items with other Panel either on major and minor axes column.

        Parameters
        ----------
        other : Panel or list of Panels
            Index should be similar to one of the columns in this one
        how : {'left', 'right', 'outer', 'inner'}
            How to handle indexes of the two objects. Default: 'left'
            for joining on index, None otherwise
            * left: use calling frame's index
            * right: use input frame's index
            * outer: form union of indexes
            * inner: use intersection of indexes
        lsuffix : string
            Suffix to use from left frame's overlapping columns
        rsuffix : string
            Suffix to use from right frame's overlapping columns

        Returns
        -------
        joined : Panel
        """
        from pandas.core.reshape.concat import concat

        if isinstance(other, Panel):
            join_major, join_minor = self._get_join_index(other, how)
            this = self.reindex(major=join_major, minor=join_minor)
            other = other.reindex(major=join_major, minor=join_minor)
            merged_data = this._data.merge(other._data, lsuffix, rsuffix)
            return self._constructor(merged_data)
        else:
            if lsuffix or rsuffix:
                raise ValueError('Suffixes not supported when passing '
                                 'multiple panels')

            if how == 'left':
                how = 'outer'
                join_axes = [self.major_axis, self.minor_axis]
            elif how == 'right':
                raise ValueError('Right join not supported with multiple '
                                 'panels')
            else:
                join_axes = None

            return concat([self] + list(other), axis=0, join=how,
                          join_axes=join_axes, verify_integrity=True)
