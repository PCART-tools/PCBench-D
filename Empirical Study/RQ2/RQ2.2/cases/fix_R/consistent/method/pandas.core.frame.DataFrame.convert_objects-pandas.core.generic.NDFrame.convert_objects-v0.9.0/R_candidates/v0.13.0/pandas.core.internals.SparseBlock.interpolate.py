    def interpolate(self, method='pad', axis=0, inplace=False,
                    limit=None, fill_value=None, **kwargs):

        values = com.interpolate_2d(
            self.values.to_dense(), method, axis, limit, fill_value)
        return self.make_block(values, self.items, self.ref_items)
