    @Appender(_index_shared_docs["repeat"] % _index_doc_kwargs)
    def repeat(self, repeats, axis=None):
        repeats = ensure_platform_int(repeats)
        nv.validate_repeat((), {"axis": axis})
        res_values = self._values.repeat(repeats)

        # _constructor so RangeIndex-> Index with an int64 dtype
        return self._constructor._simple_new(res_values, name=self.name)
