def safe_take(n, b):
    r = list(take(n, b))
    if len(r) != n:
        warn("Insufficient elements for `take`. {0} elements requested, "
             "only {1} elements available. Try passing larger `npartitions` "
             "to `take`.".format(n, len(r)))
    return r
