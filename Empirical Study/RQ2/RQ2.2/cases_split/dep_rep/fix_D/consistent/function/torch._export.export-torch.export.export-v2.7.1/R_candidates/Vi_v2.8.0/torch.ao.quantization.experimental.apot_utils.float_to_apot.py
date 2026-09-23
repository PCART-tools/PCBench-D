def float_to_apot(x, levels, indices, alpha):
    # clip values based on alpha
    if x < -alpha:
        return -alpha
    elif x > alpha:
        return alpha

    levels_lst = list(levels)
    indices_lst = list(indices)

    min_delta = math.inf
    best_idx = 0

    for level, idx in zip(levels_lst, indices_lst):
        cur_delta = abs(level - x)
        if cur_delta < min_delta:
            min_delta = cur_delta
            best_idx = idx

    return best_idx
