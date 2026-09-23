    def dropna(self, axis=0, how='any', inplace=False):
        """
        Drop 2D from panel, holding passed axis constant.

        Parameters
        ----------
        axis : int, default 0
            Axis to hold constant. E.g. axis=1 will drop major_axis entries
            having a certain amount of NA data
        how : {'all', 'any'}, default 'any'
            'any': one or more values are NA in the DataFrame along the
            axis. For 'all' they all must be.
        inplace : bool, default False
            If True, do operation inplace and return None.

        Returns
        -------
        dropped : Panel
        """
        axis = self._get_axis_number(axis)

        values = self.values
        mask = notna(values)

        for ax in reversed(sorted(set(range(self._AXIS_LEN)) - {axis})):
            mask = mask.sum(ax)

        per_slice = np.prod(values.shape[:axis] + values.shape[axis + 1:])

        if how == 'all':
            cond = mask > 0
        else:
            cond = mask == per_slice

        new_ax = self._get_axis(axis)[cond]
        result = self.reindex_axis(new_ax, axis=axis)
        if inplace:
            self._update_inplace(result)
        else:
            return result
