    def interpolate(self, method='pad', axis=0, inplace=False,
                    limit=None, fill_value=None, **kwargs):

        values = self.values if inplace else self.values.copy()
        return self.make_block_same_class(values=values.fillna(fill_value=fill_value,
                                                               method=method,
                                                               limit=limit),
                                          placement=self.mgr_locs)
