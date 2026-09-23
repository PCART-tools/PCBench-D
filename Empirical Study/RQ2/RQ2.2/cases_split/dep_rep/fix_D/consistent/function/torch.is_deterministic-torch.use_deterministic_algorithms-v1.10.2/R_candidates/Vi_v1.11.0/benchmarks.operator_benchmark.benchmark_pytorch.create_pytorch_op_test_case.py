def create_pytorch_op_test_case(op_bench, test_config):
    """ This method is used to generate est. func_name is a global unique
    string. For PyTorch add operator with M=8, N=2, K=1, tag = long, here
    are the values for the members in test_case:
    op.module_name: add
    framework: PyTorch
    test_config: TestConfig(test_name='add_M8_N2_K1', input_config='M: 8, N: 2, K: 1',
        tag='long', run_backward=False)
    func_name: addPyTorchTestConfig(test_name='add_M8_N2_K1', input_config='M: 8, N: 2, K: 1',
                                    tag='long', run_backward=False)
    """
    test_case = PyTorchOperatorTestCase(op_bench, test_config)
    test_config = test_case.test_config
    op = test_case.op_bench
    func_name = "{}{}{}".format(op.module_name(), test_case.framework, str(test_config))
    return (func_name, test_case)
