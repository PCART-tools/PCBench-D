    def fillna(self, value, limit=None, inplace=False, downcast=None):
        # we may need to upcast our fill to match our dtype
        if limit is not None:
            raise NotImplementedError
        if issubclass(self.dtype.type, np.floating):
            value = float(value)
        values = self.values if inplace else self.values.copy()
        return [self.make_block_same_class(values=values.get_values(value),
                                           fill_value=value,
                                           placement=self.mgr_locs)]
