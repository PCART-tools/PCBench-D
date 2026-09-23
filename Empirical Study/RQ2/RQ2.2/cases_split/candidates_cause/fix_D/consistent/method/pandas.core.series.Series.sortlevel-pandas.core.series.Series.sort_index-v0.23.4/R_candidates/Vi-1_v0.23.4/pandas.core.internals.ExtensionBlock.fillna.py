    def fillna(self, value, limit=None, inplace=False, downcast=None,
               mgr=None):
        values = self.values if inplace else self.values.copy()
        values = values.fillna(value=value, limit=limit)
        return [self.make_block_same_class(values=values,
                                           placement=self.mgr_locs,
                                           ndim=self.ndim)]
