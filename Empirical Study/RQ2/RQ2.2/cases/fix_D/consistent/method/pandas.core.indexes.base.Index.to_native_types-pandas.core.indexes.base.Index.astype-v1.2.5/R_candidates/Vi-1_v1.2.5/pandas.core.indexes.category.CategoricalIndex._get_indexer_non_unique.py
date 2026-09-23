    def _get_indexer_non_unique(self, values: ArrayLike):
        """
        get_indexer_non_unique but after unrapping the target Index object.
        """
        # Note: we use engine.get_indexer_non_unique for get_indexer in addition
        #  to get_indexer_non_unique because, even if `target` is unique, any
        #  non-category entries in it will be encoded as -1  so `codes` may
        #  not be unique.

        if isinstance(values, Categorical):
            # Indexing on codes is more efficient if categories are the same,
            #  so we can apply some optimizations based on the degree of
            #  dtype-matching.
            cat = self._data._encode_with_my_categories(values)
            codes = cat._codes
        else:
            codes = self.categories.get_indexer(values)

        indexer, missing = self._engine.get_indexer_non_unique(codes)
        return ensure_platform_int(indexer), missing
