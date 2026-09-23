    @Appender(_index_shared_docs['repeat'] % _index_doc_kwargs)
    def repeat(self, repeats, axis=None):
        nv.validate_repeat(tuple(), dict(axis=axis))
        return MultiIndex(levels=self.levels,
                          codes=[level_codes.view(np.ndarray).repeat(repeats)
                                 for level_codes in self.codes],
                          names=self.names, sortorder=self.sortorder,
                          verify_integrity=False)
