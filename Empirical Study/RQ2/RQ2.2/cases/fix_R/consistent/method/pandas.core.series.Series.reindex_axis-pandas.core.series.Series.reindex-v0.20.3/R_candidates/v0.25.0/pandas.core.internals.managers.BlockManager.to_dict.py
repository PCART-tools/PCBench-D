    def to_dict(self, copy=True):
        """
        Return a dict of str(dtype) -> BlockManager

        Parameters
        ----------
        copy : boolean, default True

        Returns
        -------
        values : a dict of dtype -> BlockManager

        Notes
        -----
        This consolidates based on str(dtype)
        """
        self._consolidate_inplace()

        bd = {}
        for b in self.blocks:
            bd.setdefault(str(b.dtype), []).append(b)

        return {dtype: self.combine(blocks, copy=copy) for dtype, blocks in bd.items()}
