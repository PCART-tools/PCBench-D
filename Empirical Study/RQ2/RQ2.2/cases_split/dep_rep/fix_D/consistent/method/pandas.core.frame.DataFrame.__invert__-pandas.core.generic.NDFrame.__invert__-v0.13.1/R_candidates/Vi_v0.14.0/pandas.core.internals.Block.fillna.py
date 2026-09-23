    def fillna(self, value, limit=None, inplace=False, downcast=None):
        if not self._can_hold_na:
            if inplace:
                return [self]
            else:
                return [self.copy()]

        mask = isnull(self.values)
        if limit is not None:
            if self.ndim > 2:
                raise NotImplementedError
            mask[mask.cumsum(self.ndim-1)>limit]=False

        value = self._try_fill(value)
        blocks = self.putmask(mask, value, inplace=inplace)
        return self._maybe_downcast(blocks, downcast)
