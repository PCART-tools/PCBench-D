def make_group(k, stage):
    def h(x):
        return x[0] // k ** stage % k
    return h
