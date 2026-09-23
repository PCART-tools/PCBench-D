def mse(x, xh):
    d = (x - xh).reshape(-1)
    return 0 if len(d) == 0 else np.sqrt(np.matmul(d, d.transpose())) / len(d)
