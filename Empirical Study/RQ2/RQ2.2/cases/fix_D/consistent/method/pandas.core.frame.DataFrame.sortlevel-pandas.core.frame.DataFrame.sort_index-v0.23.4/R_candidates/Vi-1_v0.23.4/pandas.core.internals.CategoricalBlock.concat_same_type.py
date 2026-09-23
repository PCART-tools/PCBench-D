    def concat_same_type(self, to_concat, placement=None):
        """
        Concatenate list of single blocks of the same type.

        Note that this CategoricalBlock._concat_same_type *may* not
        return a CategoricalBlock. When the categories in `to_concat`
        differ, this will return an object ndarray.

        If / when we decide we don't like that behavior:

        1. Change Categorical._concat_same_type to use union_categoricals
        2. Delete this method.
        """
        values = self._concatenator([blk.values for blk in to_concat],
                                    axis=self.ndim - 1)
        # not using self.make_block_same_class as values can be object dtype
        return make_block(
            values, placement=placement or slice(0, len(values), 1),
            ndim=self.ndim)
