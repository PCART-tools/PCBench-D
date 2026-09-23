def mux(select, left, right):
    return [np.vectorize(lambda c, x, y: x if c else y)(select, left, right)]
