def _generate_test_points(typecodes):
    axes = tuple(map(lambda x: TEST_POINTS[x], typecodes))
    pts = list(product(*axes))
    return pts
