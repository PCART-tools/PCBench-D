    def to_sparse(self, fill_value=None, kind='block'):
        """
        Convert to SparsePanel

        Parameters
        ----------
        fill_value : float, default NaN
        kind : {'block', 'integer'}

        Returns
        -------
        y : SparseDataFrame
        """
        from pandas.core.sparse import SparsePanel
        frames = dict(compat.iteritems(self))
        return SparsePanel(frames, items=self.items,
                           major_axis=self.major_axis,
                           minor_axis=self.minor_axis,
                           default_kind=kind,
                           default_fill_value=fill_value)
