def jsd_grad(go, o, pq_list):
    p, q = pq_list
    m = (p + q) / 2.
    return [np.log(p * (1 - m) / (1 - p) / m) / 2. * go, None]
