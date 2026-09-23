def _make_agg_id(func, column):
    return '{!s}-{!s}-{}'.format(func, column, tokenize(func, column))
