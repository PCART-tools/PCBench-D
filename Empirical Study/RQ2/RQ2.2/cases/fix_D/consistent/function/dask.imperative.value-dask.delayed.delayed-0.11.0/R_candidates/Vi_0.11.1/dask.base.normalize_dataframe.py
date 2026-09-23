    @partial(normalize_token.register, pd.DataFrame)
    def normalize_dataframe(df):
        data = [block.values for block in df._data.blocks]
        data += [df.columns, df.index]
        return list(map(normalize_token, data))
