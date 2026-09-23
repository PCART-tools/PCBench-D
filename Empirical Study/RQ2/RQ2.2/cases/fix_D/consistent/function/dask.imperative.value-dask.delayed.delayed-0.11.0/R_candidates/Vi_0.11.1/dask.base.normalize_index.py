    @partial(normalize_token.register, pd.Index)
    def normalize_index(ind):
        return [ind.name, normalize_token(ind.values)]
