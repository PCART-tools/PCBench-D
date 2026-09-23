def register_broadcast_ops():
    binary_op_list = [
        ["mul", lambda a, b: a * b],
        ["add", lambda a, b: a + b],
        ["sub", lambda a, b: a - b],
        ["div", lambda a, b: a / (b + 1e-4)],
        [
            "pow",
            lambda a, b: torch.pow(a, b),
            lambda a, b: np.power(a, b),
        ],  # no fuson triggered
        ["max", lambda a, b: torch.max(a, b), lambda a, b: np.maximum(a, b)],
        ["min", lambda a, b: torch.min(a, b), lambda a, b: np.minimum(a, b)],
    ]

    unary_op_list = [
        ["erf", lambda x: torch.erf(x), lambda x: np.erf(x)],
        ["exp", lambda x: torch.exp(x), lambda x: np.exp(x)],
        ["sin", lambda x: torch.sin(x), lambda x: np.sin(x)],
        ["cos", lambda x: torch.cos(x), lambda x: np.cos(x)],
    ]

    for split_input, binary_op in itertools.product([True, False], binary_op_list):
        # Make a copy of BroadcastBench
        if len(binary_op) == 2:
            [op_str, op_pt_func] = binary_op
            op_np_func = op_pt_func
        elif len(binary_op) == 3:
            [op_str, op_pt_func, op_np_func] = binary_op
        split_str = "split" if split_input else "shared"
        op_str = split_str + "_" + op_str
        bm_cls = type("BroadcastBench_" + op_str, (BroadcastBench,), {})
        bm_cls.op_str = op_str
        bm_cls.binary_op_pt_func = op_pt_func
        bm_cls.binary_op_np_func = op_np_func
        bm_cls.split_input = split_input
        benchmark.register_benchmark_class(bm_cls)

    for split_input, unary_op in itertools.product([True, False], unary_op_list):
        # Make a copy of BroadcastBench
        if len(unary_op) == 2:
            [op_str, op_pt_func] = unary_op
            op_np_func = op_pt_func
        elif len(unary_op) == 3:
            [op_str, op_pt_func, op_np_func] = unary_op
        split_str = "split" if split_input else "shared"
        op_str = split_str + "_" + op_str
        bm_cls = type("BroadcastBench_" + op_str, (BroadcastBench,), {})
        bm_cls.op_str = op_str
        bm_cls.unary_op_pt_func = op_pt_func
        bm_cls.unary_op_np_func = op_np_func
        bm_cls.split_input = split_input
        benchmark.register_benchmark_class(bm_cls)
