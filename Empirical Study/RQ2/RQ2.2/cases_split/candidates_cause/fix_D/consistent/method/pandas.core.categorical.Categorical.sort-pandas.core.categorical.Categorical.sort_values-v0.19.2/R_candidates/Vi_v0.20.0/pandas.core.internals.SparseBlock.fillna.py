    def fillna(self, value, limit=None, inplace=False, downcast=None,
               mgr=None):
        # we may need to upcast our fill to match our dtype
        if limit is not None:
            raise NotImplementedError("specifying a limit for 'fillna' has "
                                      "not been implemented yet")
        values = self.values if inplace else self.values.copy()
        values = values.fillna(value, downcast=downcast)
        return [self.make_block_same_class(values=values,
                                           placement=self.mgr_locs)]
