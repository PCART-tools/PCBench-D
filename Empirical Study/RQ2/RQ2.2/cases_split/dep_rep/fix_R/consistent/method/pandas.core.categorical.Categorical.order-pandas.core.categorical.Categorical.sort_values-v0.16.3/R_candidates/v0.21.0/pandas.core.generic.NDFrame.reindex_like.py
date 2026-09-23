    def reindex_like(self, other, method=None, copy=True, limit=None,
                     tolerance=None):
        """Return an object with matching indices to myself.

        Parameters
        ----------
        other : Object
        method : string or None
        copy : boolean, default True
        limit : int, default None
            Maximum number of consecutive labels to fill for inexact matches.
        tolerance : optional
            Maximum distance between labels of the other object and this
            object for inexact matches. Can be list-like.

            .. versionadded:: 0.17.0
            .. versionadded:: 0.21.0 (list-like tolerance)

        Notes
        -----
        Like calling s.reindex(index=other.index, columns=other.columns,
                               method=...)

        Returns
        -------
        reindexed : same as input
        """
        d = other._construct_axes_dict(axes=self._AXIS_ORDERS, method=method,
                                       copy=copy, limit=limit,
                                       tolerance=tolerance)

        return self.reindex(**d)
