def sphere_decreasing(middle, pos):
    return 1.0 - sqrt(1.0 - linear(middle, pos) ** 2)
