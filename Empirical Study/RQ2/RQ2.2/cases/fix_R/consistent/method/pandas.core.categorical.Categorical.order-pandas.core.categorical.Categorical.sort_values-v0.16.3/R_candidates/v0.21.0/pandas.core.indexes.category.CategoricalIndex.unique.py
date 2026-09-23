    @Appender(base._shared_docs['unique'] % _index_doc_kwargs)
    def unique(self):
        result = base.IndexOpsMixin.unique(self)
        # CategoricalIndex._shallow_copy uses keeps original categories
        # and ordered if not otherwise specified
        return self._shallow_copy(result, categories=result.categories,
                                  ordered=result.ordered)
