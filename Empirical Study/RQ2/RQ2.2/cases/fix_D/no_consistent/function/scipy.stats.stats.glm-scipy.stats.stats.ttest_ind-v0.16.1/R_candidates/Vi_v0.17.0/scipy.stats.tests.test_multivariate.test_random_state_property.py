def test_random_state_property():
    scale = np.eye(3)
    scale[0, 1] = 0.5
    scale[1, 0] = 0.5
    dists = [
        [multivariate_normal, ()],
        [dirichlet, (np.array([1.]), )],
        [wishart, (10, scale)],
        [invwishart, (10, scale)]
    ]
    for distfn, args in dists:
        check_random_state_property(distfn, args)
        check_pickling(distfn, args)
