    def diff(self, periods=1, axis=0):
        """
        1st discrete difference of object

        Parameters
        ----------
        periods : int, default 1
            Periods to shift for forming difference
        axis : {0 or 'index', 1 or 'columns'}, default 0
            Take difference over rows (0) or columns (1).

            .. versionadded: 0.16.1

        Returns
        -------
        diffed : DataFrame
        """
        bm_axis = self._get_block_manager_axis(axis)
        new_data = self._data.diff(n=periods, axis=bm_axis)
        return self._constructor(new_data)
