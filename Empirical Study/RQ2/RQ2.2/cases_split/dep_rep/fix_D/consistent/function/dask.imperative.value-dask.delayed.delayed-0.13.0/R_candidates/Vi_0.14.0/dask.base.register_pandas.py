@normalize_token.register_lazy("pandas")
def register_pandas():
    import pandas as pd

    @normalize_token.register(pd.Index)
    def normalize_index(ind):
        return [ind.name, normalize_token(ind.values)]

    @normalize_token.register(pd.Categorical)
    def normalize_categorical(cat):
        return [normalize_token(cat.codes),
                normalize_token(cat.categories),
                cat.ordered]

    @normalize_token.register(pd.Series)
    def normalize_series(s):
        return [s.name, s.dtype,
                normalize_token(s._data.blocks[0].values),
                normalize_token(s.index)]

    @normalize_token.register(pd.DataFrame)
    def normalize_dataframe(df):
        data = [block.values for block in df._data.blocks]
        data += [df.columns, df.index]
        return list(map(normalize_token, data))
