    def fillna(self, value, limit=None, inplace=False, downcast=None,
               mgr=None):
        """ fillna on the block with the value. If we fail, then convert to
        ObjectBlock and try again
        """

        if not self._can_hold_na:
            if inplace:
                return self
            else:
                return self.copy()

        original_value = value
        mask = isnull(self.values)
        if limit is not None:
            if self.ndim > 2:
                raise NotImplementedError("number of dimensions for 'fillna' "
                                          "is currently limited to 2")
            mask[mask.cumsum(self.ndim - 1) > limit] = False

        # fillna, but if we cannot coerce, then try again as an ObjectBlock
        try:
            values, _, value, _ = self._try_coerce_args(self.values, value)
            blocks = self.putmask(mask, value, inplace=inplace)
            blocks = [b.make_block(values=self._try_coerce_result(b.values))
                      for b in blocks]
            return self._maybe_downcast(blocks, downcast)
        except (TypeError, ValueError):

            # we can't process the value, but nothing to do
            if not mask.any():
                return self if inplace else self.copy()

            # we cannot coerce the underlying object, so
            # make an ObjectBlock
            return self.to_object_block(mgr=mgr).fillna(original_value,
                                                        limit=limit,
                                                        inplace=inplace,
                                                        downcast=False)
