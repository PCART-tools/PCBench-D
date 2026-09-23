def _get_distinct_indexes(indexes):
    return list(dict((id(x), x) for x in indexes).values())
