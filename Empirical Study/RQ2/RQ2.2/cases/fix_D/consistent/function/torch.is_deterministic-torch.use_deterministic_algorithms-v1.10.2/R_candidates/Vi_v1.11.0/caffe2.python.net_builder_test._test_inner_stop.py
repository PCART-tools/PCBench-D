def _test_inner_stop(x):
    ops.stop_if(ops.LT([x, ops.Const(5)]))
