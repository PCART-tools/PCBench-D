def create_caffe2_op_test_case(op_bench, test_config):
    test_case = Caffe2OperatorTestCase(op_bench, test_config)
    test_config = test_case.test_config
    op = test_case.op_bench
    func_name = "{}{}{}".format(op.module_name(), test_case.framework, str(test_config))
    return (func_name, test_case)
