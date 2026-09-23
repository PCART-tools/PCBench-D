def _equal_var_ttest_denom(v1, n1, v2, n2):
    df = n1 + n2 - 2
    svar = ((n1 - 1) * v1 + (n2 - 1) * v2) / float(df)
    denom = np.sqrt(svar * (1.0 / n1 + 1.0 / n2))
    return df, denom
