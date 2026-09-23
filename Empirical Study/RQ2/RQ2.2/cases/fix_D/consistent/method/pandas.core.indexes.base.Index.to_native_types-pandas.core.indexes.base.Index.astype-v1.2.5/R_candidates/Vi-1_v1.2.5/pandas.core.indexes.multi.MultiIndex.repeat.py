    @Appender(_index_shared_docs["repeat"] % _index_doc_kwargs)
    def repeat(self, repeats, axis=None):
        nv.validate_repeat((), {"axis": axis})
        repeats = ensure_platform_int(repeats)
        return MultiIndex(
            levels=self.levels,
            codes=[
                level_codes.view(np.ndarray).astype(np.intp).repeat(repeats)
                for level_codes in self.codes
            ],
            names=self.names,
            sortorder=self.sortorder,
            verify_integrity=False,
        )
