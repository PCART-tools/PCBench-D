def gen_boxes(count, center):
    len = 10
    len_half = len / 2.0
    ret = np.tile(
        np.array(
            [center[0] - len_half, center[1] - len_half,
            center[0] + len_half, center[1] + len_half]
        ).astype(np.float32),
        (count, 1)
    )
    return ret
