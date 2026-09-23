def is_dictlike(x):
    return isinstance(x, (dict, com.ABCSeries))
