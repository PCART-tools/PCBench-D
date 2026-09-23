    def diff(self, periods=1):
        """
        1st discrete difference of object

        Parameters
        ----------
        periods : int, default 1
            Periods to shift for forming difference

        Returns
        -------
        diffed : DataFrame
        """
        new_data = self._data.diff(n=periods)
        return self._constructor(new_data)
