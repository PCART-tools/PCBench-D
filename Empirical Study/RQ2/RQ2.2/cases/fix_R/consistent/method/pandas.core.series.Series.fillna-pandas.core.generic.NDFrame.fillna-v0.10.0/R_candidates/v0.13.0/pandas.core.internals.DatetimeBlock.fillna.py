    def fillna(self, value, inplace=False, downcast=None):
        # straight putmask here
        values = self.values if inplace else self.values.copy()
        mask = com.isnull(self.values)
        value = self._try_fill(value)
        np.putmask(values, mask, value)
        return [self if inplace else
                make_block(values, self.items, self.ref_items, fastpath=True)]
