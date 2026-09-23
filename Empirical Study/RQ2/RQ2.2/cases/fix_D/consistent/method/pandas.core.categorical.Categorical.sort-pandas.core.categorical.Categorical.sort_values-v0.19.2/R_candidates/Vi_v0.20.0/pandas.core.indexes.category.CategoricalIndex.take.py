    @Appender(_index_shared_docs['take'] % _index_doc_kwargs)
    def take(self, indices, axis=0, allow_fill=True,
             fill_value=None, **kwargs):
        nv.validate_take(tuple(), kwargs)
        indices = _ensure_platform_int(indices)
        taken = self._assert_take_fillable(self.codes, indices,
                                           allow_fill=allow_fill,
                                           fill_value=fill_value,
                                           na_value=-1)
        return self._create_from_codes(taken)
