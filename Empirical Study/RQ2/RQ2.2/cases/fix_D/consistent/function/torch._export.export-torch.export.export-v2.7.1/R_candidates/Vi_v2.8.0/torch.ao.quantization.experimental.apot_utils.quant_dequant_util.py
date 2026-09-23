def quant_dequant_util(x, levels, indices):
    min_delta = math.inf
    best_fp = 0.0

    for level in levels:
        cur_delta = abs(level - x)
        if cur_delta < min_delta:
            min_delta = cur_delta
            best_fp = level

    return best_fp
