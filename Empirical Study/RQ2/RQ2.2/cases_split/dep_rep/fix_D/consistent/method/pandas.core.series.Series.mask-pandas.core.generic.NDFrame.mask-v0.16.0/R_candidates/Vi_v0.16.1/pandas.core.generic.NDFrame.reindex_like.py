    def reindex_like(self, other, method=None, copy=True, limit=None):
        """ return an object with matching indicies to myself

        Parameters
        ----------
        other : Object
        method : string or None
        copy : boolean, default True
        limit : int, default None
            Maximum size gap to forward or backward fill

        Notes
        -----
        Like calling s.reindex(index=other.index, columns=other.columns,
                               method=...)

        Returns
        -------
        reindexed : same as input
        """
        d = other._construct_axes_dict(axes=self._AXIS_ORDERS,
                method=method, copy=copy, limit=limit)

        return self.reindex(**d)
