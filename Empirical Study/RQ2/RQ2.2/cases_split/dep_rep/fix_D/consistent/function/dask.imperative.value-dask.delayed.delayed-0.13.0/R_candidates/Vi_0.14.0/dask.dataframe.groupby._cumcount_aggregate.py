def _cumcount_aggregate(a, b, fill_value=None):
    return a.add(b, fill_value=fill_value) + 1
