def curved(middle, pos):
    return pos ** (log(0.5) / log(max(middle, EPSILON)))
