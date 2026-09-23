def _sum_of_list(tensorlist):
    s = 0
    for t in tensorlist:
        s += t.sum()
    return s
