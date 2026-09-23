def shifted_sum(df, before, after, c=0):
    a = df.shift(before)
    b = df.shift(-after)
    return df + a + b + c
