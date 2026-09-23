def test_stacklimit():
    dsk = dict(('x%s' % (i + 1), (inc, 'x%s' % i)) for i in range(10000))
    dependencies, dependents = get_deps(dsk)
    scores = dict.fromkeys(dsk, 1)
    child_max(dependencies, dependents, scores)
    ndependents(dependencies, dependents)
