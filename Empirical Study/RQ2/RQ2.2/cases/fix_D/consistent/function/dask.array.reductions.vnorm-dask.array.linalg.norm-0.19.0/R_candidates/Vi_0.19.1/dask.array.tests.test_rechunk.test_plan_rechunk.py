def test_plan_rechunk():
    c = ((20,) * 2)              # coarse
    f = ((2,) * 20)              # fine
    nc = ((float('nan'),) * 2)   # nan-coarse
    nf = ((float('nan'),) * 20)  # nan-fine

    # Trivial cases
    steps = _plan((), ())
    _assert_steps(steps, [()])
    steps = _plan((c, ()), (f, ()))
    _assert_steps(steps, [(f, ())])

    # No intermediate required
    steps = _plan((c,), (f,))
    _assert_steps(steps, [(f,)])
    steps = _plan((f,), (c,))
    _assert_steps(steps, [(c,)])
    steps = _plan((c, c), (f, f))
    _assert_steps(steps, [(f, f)])
    steps = _plan((f, f), (c, c))
    _assert_steps(steps, [(c, c)])
    steps = _plan((f, c), (c, c))
    _assert_steps(steps, [(c, c)])

    # An intermediate is used to reduce graph size
    steps = _plan((f, c), (c, f))
    _assert_steps(steps, [(c, c), (c, f)])

    steps = _plan((c + c, c + f), (f + f, c + c))
    _assert_steps(steps, [(c + c, c + c), (f + f, c + c)])

    # Same, with unknown dim
    steps = _plan((nc + nf, c + c, c + f), (nc + nf, f + f, c + c))
    _assert_steps(steps, steps)

    # Just at the memory limit => an intermediate is used
    steps = _plan((f, c), (c, f), block_size_limit=400)
    _assert_steps(steps, [(c, c), (c, f)])

    # Hitting the memory limit => partial merge
    m = ((10,) * 4)   # mid

    steps = _plan((f, c), (c, f), block_size_limit=399)
    _assert_steps(steps, [(m, c), (c, f)])

    steps2 = _plan((f, c), (c, f), block_size_limit=3999, itemsize=10)
    _assert_steps(steps2, steps)

    # Larger problem size => more intermediates
    c = ((1000,) * 2)   # coarse
    f = ((2,) * 1000)   # fine

    steps = _plan((f, c), (c, f), block_size_limit=99999)
    assert len(steps) == 3
    assert steps[-1] == (c, f)
    for i in range(len(steps) - 1):
        prev = steps[i]
        succ = steps[i + 1]
        # Merging on the first dim, splitting on the second dim
        assert len(succ[0]) <= len(prev[0]) / 2.0
        assert len(succ[1]) >= len(prev[1]) * 2.0
