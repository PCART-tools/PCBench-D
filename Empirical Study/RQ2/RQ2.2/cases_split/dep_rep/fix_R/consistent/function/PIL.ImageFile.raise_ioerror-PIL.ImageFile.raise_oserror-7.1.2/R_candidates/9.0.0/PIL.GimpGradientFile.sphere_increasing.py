def sphere_increasing(middle, pos):
    return sqrt(1.0 - (linear(middle, pos) - 1.0) ** 2)
