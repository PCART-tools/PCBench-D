    @Appender(_index_shared_docs['_shallow_copy'])
    def _shallow_copy(self, values=None, categories=None, ordered=None,
                      dtype=None, **kwargs):
        # categories and ordered can't be part of attributes,
        # as these are properties
        # we want to reuse self.dtype if possible, i.e. neither are
        # overridden.
        if dtype is not None and (categories is not None or
                                  ordered is not None):
            raise TypeError("Cannot specify both `dtype` and `categories` "
                            "or `ordered`")

        if categories is None and ordered is None:
            dtype = self.dtype if dtype is None else dtype
            return super(CategoricalIndex, self)._shallow_copy(
                values=values, dtype=dtype, **kwargs)
        if categories is None:
            categories = self.categories
        if ordered is None:
            ordered = self.ordered

        return super(CategoricalIndex, self)._shallow_copy(
            values=values, categories=categories,
            ordered=ordered, **kwargs)
