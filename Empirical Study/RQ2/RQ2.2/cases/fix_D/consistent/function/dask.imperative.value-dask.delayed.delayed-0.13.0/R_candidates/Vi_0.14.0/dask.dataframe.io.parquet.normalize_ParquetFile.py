    @partial(normalize_token.register, fastparquet.ParquetFile)
    def normalize_ParquetFile(pf):
        return (type(pf), pf.fn, pf.sep) + normalize_token(pf.open)
