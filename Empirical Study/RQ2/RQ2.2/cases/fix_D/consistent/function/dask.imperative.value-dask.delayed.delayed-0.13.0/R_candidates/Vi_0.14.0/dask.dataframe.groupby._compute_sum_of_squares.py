def _compute_sum_of_squares(grouped, column):
    base = grouped[column] if column is not None else grouped
    return base.apply(lambda x: (x ** 2).sum())
