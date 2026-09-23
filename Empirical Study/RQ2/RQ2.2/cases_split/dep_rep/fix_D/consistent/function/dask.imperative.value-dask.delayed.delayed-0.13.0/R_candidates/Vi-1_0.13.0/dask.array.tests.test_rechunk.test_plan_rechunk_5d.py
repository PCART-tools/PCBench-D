def test_plan_rechunk_5d():
    # 5d problem
    c = ((10,) * 1)    # coarse
    f = ((1,) * 10)    # fine

    steps = _plan((c, c, c, c, c), (f, f, f, f, f))
    _assert_steps(steps, [(f, f, f, f, f)])
    steps = _plan((f, f, f, f, c), (c, c, c, f, f))
    _assert_steps(steps, [(c, c, c, f, c), (c, c, c, f, f)])
    # Only 1 dim can be merged at first
    steps = _plan((c, c, f, f, c), (c, c, c, f, f), block_size_limit=2e4)
    _assert_steps(steps, [(c, c, c, f, c), (c, c, c, f, f)])
