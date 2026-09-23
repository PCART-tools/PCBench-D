def _get_categories(x):
    return x.cat.categories if isinstance(x, pd.Series) else x.categories
