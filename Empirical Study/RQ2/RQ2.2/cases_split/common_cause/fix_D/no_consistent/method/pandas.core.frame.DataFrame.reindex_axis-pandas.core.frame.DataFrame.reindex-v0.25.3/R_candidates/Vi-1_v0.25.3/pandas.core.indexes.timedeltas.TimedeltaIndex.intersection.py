    def intersection(self, other, sort=False):
        """
        Specialized intersection for TimedeltaIndex objects.
        May be much faster than Index.intersection

        Parameters
        ----------
        other : TimedeltaIndex or array-like
        sort : False or None, default False
            Sort the resulting index if possible.

            .. versionadded:: 0.24.0

            .. versionchanged:: 0.24.1

               Changed the default to ``False`` to match the behaviour
               from before 0.24.0.

            .. versionchanged:: 0.25.0

               The `sort` keyword is added

        Returns
        -------
        y : Index or  TimedeltaIndex
        """
        return super().intersection(other, sort=sort)
