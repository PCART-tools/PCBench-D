def loop_graph(a, b, iters: int):
    c = a + b * 2
    for i in range(iters):
        c = c + b
        c *= 2
        c -= a
    return c
