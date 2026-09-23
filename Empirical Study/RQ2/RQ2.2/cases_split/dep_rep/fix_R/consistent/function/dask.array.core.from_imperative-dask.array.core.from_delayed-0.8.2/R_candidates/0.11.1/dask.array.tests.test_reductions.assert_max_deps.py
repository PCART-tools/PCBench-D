def assert_max_deps(x, n, eq=True):
    dependencies, dependents = get_deps(x.dask)
    if eq:
        assert max(map(len, dependencies.values())) == n
    else:
        assert max(map(len, dependencies.values())) <= n
