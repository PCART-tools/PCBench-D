def _int64_overflow_possible(shape):
    the_prod = long(1)
    for x in shape:
        the_prod *= long(x)

    return the_prod >= _INT64_MAX
