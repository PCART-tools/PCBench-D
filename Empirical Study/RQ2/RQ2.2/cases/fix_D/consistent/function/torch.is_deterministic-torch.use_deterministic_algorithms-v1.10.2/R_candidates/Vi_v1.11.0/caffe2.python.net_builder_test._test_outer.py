def _test_outer():
    x = ops.Const(10)
    # test stop_if(False)
    with ops.stop_guard() as g1:
        _test_inner_stop(x)

    # test stop_if(True)
    y = ops.Const(3)
    with ops.stop_guard() as g2:
        _test_inner_stop(y)

    # test no stop
    with ops.stop_guard() as g4:
        ops.Const(0)

    # test empty clause
    with ops.stop_guard() as g3:
        pass

    return (
        g1.has_stopped(), g2.has_stopped(), g3.has_stopped(), g4.has_stopped())
