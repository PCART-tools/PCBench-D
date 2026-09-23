def compute_ulp_error(opname, xvec, y_nnpi):
    y_acc = _acc_func(opname, np.float64(xvec))
    scale = 1. / _get_ulp16(y_acc)
    return (y_nnpi - y_acc) * scale
