def _count_compat(x, axis=0):
    return x.count()  # .size != .count(); count excludes nan
