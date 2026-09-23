def test_all_distributions():
    for dist in dists:
        distfunc = getattr(stats, dist)
        nargs = distfunc.numargs
        alpha = 0.01
        if dist == 'fatiguelife':
            alpha = 0.001

        if dist == 'frechet':
            args = tuple(2*rand(1))+(0,)+tuple(2*rand(2))
        elif dist == 'triang':
            args = tuple(rand(nargs))
        elif dist == 'reciprocal':
            vals = rand(nargs)
            vals[1] = vals[0] + 1.0
            args = tuple(vals)
        elif dist == 'vonmises':
            yield check_distribution, dist, (10,), alpha
            yield check_distribution, dist, (101,), alpha
            args = tuple(1.0+rand(nargs))
        else:
            args = tuple(1.0+rand(nargs))

        yield check_distribution, dist, args, alpha
