    def diff(self, periods=1):
        """
        1st discrete difference of object

        Parameters
        ----------
        periods : int, default 1
            Periods to shift for forming difference

        Returns
        -------
        diffed : Series
        """
        result = com.diff(_values_from_object(self), periods)
        return self._constructor(result, index=self.index).__finalize__(self)
