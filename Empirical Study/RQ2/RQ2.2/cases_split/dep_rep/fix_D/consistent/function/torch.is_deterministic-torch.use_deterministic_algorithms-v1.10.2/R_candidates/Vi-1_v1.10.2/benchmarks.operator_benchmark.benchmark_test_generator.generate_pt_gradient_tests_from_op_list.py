def generate_pt_gradient_tests_from_op_list(ops_list, configs, pt_bench_op):
    for op in ops_list:
        _register_test(configs, pt_bench_op, create_pytorch_op_test_case, True, op)
