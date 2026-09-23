def rowmux(select_vec, left, right):
    select = [[s] * len(left) for s in select_vec]
    return mux(select, left, right)
