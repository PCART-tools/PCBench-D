    def fillna(self, value, inplace=False, downcast=None):
        if not self._can_hold_na:
            if inplace:
                return [self]
            else:
                return [self.copy()]

        mask = com.isnull(self.values)
        value = self._try_fill(value)
        blocks = self.putmask(mask, value, inplace=inplace)
        return self._maybe_downcast(blocks, downcast)
