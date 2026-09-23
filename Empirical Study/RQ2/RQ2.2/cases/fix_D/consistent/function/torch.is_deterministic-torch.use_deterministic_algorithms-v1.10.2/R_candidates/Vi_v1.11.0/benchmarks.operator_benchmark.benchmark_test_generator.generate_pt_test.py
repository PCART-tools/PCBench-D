def generate_pt_test(configs, pt_bench_op):
    """ This function creates PyTorch op test based on the given operator
    """
    _register_test(configs, pt_bench_op, create_pytorch_op_test_case, False)
