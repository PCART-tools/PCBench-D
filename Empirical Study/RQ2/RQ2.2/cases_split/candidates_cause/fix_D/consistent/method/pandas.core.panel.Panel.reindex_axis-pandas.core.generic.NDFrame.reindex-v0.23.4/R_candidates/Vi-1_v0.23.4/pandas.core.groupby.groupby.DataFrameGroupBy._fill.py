    def _fill(self, direction, limit=None):
        """Overridden method to join grouped columns in output"""
        res = super(DataFrameGroupBy, self)._fill(direction, limit=limit)
        output = collections.OrderedDict(
            (grp.name, grp.grouper) for grp in self.grouper.groupings)

        from pandas import concat
        return concat((self._wrap_transformed_output(output), res), axis=1)
