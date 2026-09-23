    @Appender(_index_shared_docs['_shallow_copy'])
    def _shallow_copy(self, values=None, categories=None, ordered=None,
                      **kwargs):
        # categories and ordered can't be part of attributes,
        # as these are properties
        if categories is None:
            categories = self.categories
        if ordered is None:
            ordered = self.ordered
        return super(CategoricalIndex,
                     self)._shallow_copy(values=values, categories=categories,
                                         ordered=ordered, **kwargs)
