def concat_and_check(dfs):
    if len(set(map(len, dfs))) != 1:
        raise ValueError("Concattenated DataFrames of different lengths")
    return pd.concat(dfs, axis=1)
