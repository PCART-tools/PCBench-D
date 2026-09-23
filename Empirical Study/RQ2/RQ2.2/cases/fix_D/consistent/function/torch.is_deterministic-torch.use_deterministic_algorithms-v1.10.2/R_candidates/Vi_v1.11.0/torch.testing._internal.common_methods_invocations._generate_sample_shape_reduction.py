def _generate_sample_shape_reduction():
    shapes = ((S,), (S, S), (S, S, S))
    reductions = ('none', 'mean', 'sum')
    for s, r in product(shapes, reductions):
        yield s, r
