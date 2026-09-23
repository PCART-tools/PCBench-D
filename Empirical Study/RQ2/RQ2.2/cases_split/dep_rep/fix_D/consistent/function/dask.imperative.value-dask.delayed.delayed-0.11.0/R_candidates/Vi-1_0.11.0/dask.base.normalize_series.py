    @partial(normalize_token.register, pd.Series)
    def normalize_series(s):
        return [s.name, s.dtype,
                normalize_token(s._data.blocks[0].values),
                normalize_token(s.index)]
