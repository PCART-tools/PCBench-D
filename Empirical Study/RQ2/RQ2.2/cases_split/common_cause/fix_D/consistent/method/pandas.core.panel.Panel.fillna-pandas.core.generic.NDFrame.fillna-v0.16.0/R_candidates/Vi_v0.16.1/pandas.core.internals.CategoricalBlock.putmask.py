    def putmask(self, mask, new, align=True, inplace=False):
        """ putmask the data to the block; it is possible that we may create a
        new dtype of block

        return the resulting block(s)

        Parameters
        ----------
        mask  : the condition to respect
        new : a ndarray/object
        align : boolean, perform alignment on other/cond, default is True
        inplace : perform inplace modification, default is False

        Returns
        -------
        a new block(s), the result of the putmask
        """
        new_values = self.values if inplace else self.values.copy()
        new_values[mask] = new
        return [self.make_block_same_class(values=new_values, placement=self.mgr_locs)]
