    def intersection(self, other, sort=False):
        """
        Specialized intersection for DatetimeIndex objects.
        May be much faster than Index.intersection

        Parameters
        ----------
        other : DatetimeIndex or array-like
        sort : False or None, default False
            Sort the resulting index if possible.

            .. versionadded:: 0.24.0

            .. versionchanged:: 0.24.1

               Changed the default to ``False`` to match the behaviour
               from before 0.24.0.

        Returns
        -------
        y : Index or DatetimeIndex or TimedeltaIndex
        """
        return super().intersection(other, sort=sort)
