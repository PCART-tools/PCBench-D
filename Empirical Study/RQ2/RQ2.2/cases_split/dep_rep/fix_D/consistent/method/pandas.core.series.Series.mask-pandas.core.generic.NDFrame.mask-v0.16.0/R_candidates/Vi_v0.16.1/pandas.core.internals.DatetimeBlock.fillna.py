    def fillna(self, value, limit=None,
               inplace=False, downcast=None):

        # straight putmask here
        values = self.values if inplace else self.values.copy()
        mask = isnull(self.values)
        value = self._try_fill(value)
        if limit is not None:
            if self.ndim > 2:
                raise NotImplementedError("number of dimensions for 'fillna' "
                                          "is currently limited to 2")
            mask[mask.cumsum(self.ndim-1)>limit]=False

        np.putmask(values, mask, value)
        return [self if inplace else
                make_block(values,
                           fastpath=True, placement=self.mgr_locs)]
