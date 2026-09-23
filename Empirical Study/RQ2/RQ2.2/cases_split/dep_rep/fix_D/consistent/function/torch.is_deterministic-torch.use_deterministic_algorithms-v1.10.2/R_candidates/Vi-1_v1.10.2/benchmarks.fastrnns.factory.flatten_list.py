def flatten_list(lst):
    result = []
    for inner in lst:
        result.extend(inner)
    return result
