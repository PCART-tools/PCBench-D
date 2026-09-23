    @Appender(_index_shared_docs["repeat"] % _index_doc_kwargs)
    def repeat(self, repeats, axis=None):
        repeats = ensure_platform_int(repeats)
        nv.validate_repeat((), {"axis": axis})
        res_values = self._values.repeat(repeats)

        return type(self)._simple_new(res_values, name=self.name)
