    @Appender(_index_shared_docs["repeat"] % _index_doc_kwargs)
    def repeat(self, repeats: int, axis=None) -> MultiIndex:
        nv.validate_repeat((), {"axis": axis})
        # error: Incompatible types in assignment (expression has type "ndarray",
        # variable has type "int")
        repeats = ensure_platform_int(repeats)  # type: ignore[assignment]
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
