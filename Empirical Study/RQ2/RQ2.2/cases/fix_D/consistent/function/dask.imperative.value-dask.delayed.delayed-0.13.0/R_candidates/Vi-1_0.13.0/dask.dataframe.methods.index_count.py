def index_count(x):
    # Workaround since Index doesn't implement `.count`
    return pd.notnull(x).sum()
