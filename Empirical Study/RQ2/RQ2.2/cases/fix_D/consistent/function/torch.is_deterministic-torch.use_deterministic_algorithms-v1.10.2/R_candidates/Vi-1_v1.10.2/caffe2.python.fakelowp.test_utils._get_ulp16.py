def _get_ulp16(x):
    abs_x = np.abs(x)
    mask = (abs_x > 2.**(-14))
    abs_x = mask * abs_x + (1 - mask) * 2.**(-14)
    k = np.floor(np.log2(abs_x))
    return 2.**(k - 10)
