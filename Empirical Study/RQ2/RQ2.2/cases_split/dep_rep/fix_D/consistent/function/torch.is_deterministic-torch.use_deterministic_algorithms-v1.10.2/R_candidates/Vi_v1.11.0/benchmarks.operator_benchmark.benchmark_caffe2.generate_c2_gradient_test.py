def generate_c2_gradient_test(configs, c2_bench_op):
    """ This function creates Caffe2 op test based on the given operator
    """
    return _register_test(configs, c2_bench_op, create_caffe2_op_test_case,
                          True)
