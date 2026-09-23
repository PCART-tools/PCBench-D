def axis_vector_():
    t = (random.random(), random.random(), random.random())
    l = sum(x ** 2 for x in t) ** 0.5

    return [(1.0, 0.0, 0.0), (0.0, 1.0, 0.0), (0.0, 0.0, 1.0), tuple(x / l for x in t)]
