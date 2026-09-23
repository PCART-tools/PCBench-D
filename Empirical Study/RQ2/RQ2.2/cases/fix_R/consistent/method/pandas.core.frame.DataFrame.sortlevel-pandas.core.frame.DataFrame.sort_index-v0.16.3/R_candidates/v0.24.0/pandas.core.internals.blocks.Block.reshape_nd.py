    def reshape_nd(self, labels, shape, ref_items):
        """
        Parameters
        ----------
        labels : list of new axis labels
        shape : new shape
        ref_items : new ref_items

        return a new block that is transformed to a nd block
        """
        return _block2d_to_blocknd(values=self.get_values().T,
                                   placement=self.mgr_locs, shape=shape,
                                   labels=labels, ref_items=ref_items)
