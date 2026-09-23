def merge_and_compress_summaries(vals_and_weights):
    """Merge and sort percentile summaries that are already sorted.

    Each item is a tuple like ``(vals, weights)`` where vals and weights
    are lists.  We sort both by vals.

    Equal values will be combined, their weights summed together.
    """
    vals_and_weights = [x for x in vals_and_weights if x]
    if not vals_and_weights:
        return ()
    it = merge_sorted(*[zip(x, y) for x, y in vals_and_weights])
    vals = []
    weights = []
    vals_append = vals.append
    weights_append = weights.append
    val, weight = prev_val, prev_weight = next(it)
    for val, weight in it:
        if val == prev_val:
            prev_weight += weight
        else:
            vals_append(prev_val)
            weights_append(prev_weight)
            prev_val, prev_weight = val, weight
    if val == prev_val:
        vals_append(prev_val)
        weights_append(prev_weight)
    return vals, weights
