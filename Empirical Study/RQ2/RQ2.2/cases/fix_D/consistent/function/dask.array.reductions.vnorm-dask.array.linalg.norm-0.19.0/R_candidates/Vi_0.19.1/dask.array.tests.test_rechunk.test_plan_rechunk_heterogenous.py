def test_plan_rechunk_heterogenous():
    c = ((10,) * 1)    # coarse
    f = ((1,) * 10)    # fine
    cf = c + f
    cc = c + c
    ff = f + f
    fc = f + c

    # No intermediate required
    steps = _plan((cc, cf), (ff, ff))
    _assert_steps(steps, [(ff, ff)])
    steps = _plan((cf, fc), (ff, cf))
    _assert_steps(steps, [(ff, cf)])

    # An intermediate is used to reduce graph size
    steps = _plan((cc, cf), (ff, cc))
    _assert_steps(steps, [(cc, cc), (ff, cc)])

    steps = _plan((cc, cf, cc), (ff, cc, cf))
    _assert_steps(steps, [(cc, cc, cc), (ff, cc, cf)])

    # Imposing a memory limit => the first intermediate is constrained:
    #  * cc -> ff would increase the graph size: no
    #  * ff -> cf would increase the block size too much: no
    #  * cf -> cc fits the bill (graph size /= 10, block size neutral)
    #  * cf -> fc also fits the bill (graph size and block size neutral)
    steps = _plan((cc, ff, cf), (ff, cf, cc), block_size_limit=100)
    _assert_steps(steps, [(cc, ff, cc), (ff, cf, cc)])
