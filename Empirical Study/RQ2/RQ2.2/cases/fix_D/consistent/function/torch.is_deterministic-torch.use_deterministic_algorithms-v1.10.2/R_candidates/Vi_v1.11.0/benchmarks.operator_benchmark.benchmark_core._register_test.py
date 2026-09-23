def _register_test(*test_metainfo):
    """ save the metainfo needed to create a test. Currently test_metainfo
        takes two different inputs:
        1) This input when adds single op to the benchmark
         _register_test(configs, pt_bench_op, create_pytorch_op_test_case,
                          run_backward=True)
        2) This input when addes a list of ops to the benchmark
        _register_test(configs, pt_bench_op, create_pytorch_op_test_case,
                          run_backward=False,
                          op_name_function=op)
    """
    BENCHMARK_TESTER.append(test_metainfo)
