    @partial(normalize_token.register, pd.Categorical)
    def normalize_categorical(cat):
        return [normalize_token(cat.codes),
                normalize_token(cat.categories),
                cat.ordered]
