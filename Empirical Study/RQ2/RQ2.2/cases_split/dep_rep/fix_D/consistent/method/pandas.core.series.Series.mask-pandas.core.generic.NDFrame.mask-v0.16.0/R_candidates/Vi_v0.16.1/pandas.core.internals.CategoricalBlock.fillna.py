    def fillna(self, value, limit=None, inplace=False, downcast=None):
        # we may need to upcast our fill to match our dtype
        if limit is not None:
            raise NotImplementedError("specifying a limit for 'fillna' has "
                                      "not been implemented yet")

        values = self.values if inplace else self.values.copy()
        return [self.make_block_same_class(values=values.fillna(value=value,
                                                                limit=limit),
                                           placement=self.mgr_locs)]
