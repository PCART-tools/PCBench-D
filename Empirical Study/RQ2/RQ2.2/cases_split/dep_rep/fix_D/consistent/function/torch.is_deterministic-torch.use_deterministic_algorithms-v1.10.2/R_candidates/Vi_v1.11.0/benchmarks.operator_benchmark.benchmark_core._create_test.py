def _create_test(bench_op_obj, orig_test_attrs, tags, OperatorTestCase, run_backward, bwd_input):
    """ Create tests with the benchmark backend.
        Args:
            bench_op_obj: an object which instantiated from a subclass of
                Caffe2BenchmarkBase/TorchBenchmarkBase which includes tensor
                creation and operator execution.
            test_attrs: a dictionary includes test configs.
            tags: a attribute in test config to filter inputs
            OperatorTestCase: a named tuple to save the metadata of an test
            run_backward: a bool parameter indicating backward path
    """
    test_attrs = copy.deepcopy(orig_test_attrs)
    test_attrs = {k: str(v) for k, v in test_attrs.items()}
    ascii_test_attrs = ast.literal_eval(json.dumps(test_attrs))
    input_config = str(ascii_test_attrs)[1:-1].replace('\'', '')
    if bwd_input:
        # When auto_set is used, the test name needs to include input.
        test_attrs.update({'bwd': bwd_input})
    test_name = bench_op_obj.test_name(**test_attrs)
    test_config = TestConfig(test_name, input_config, tags, run_backward)
    return OperatorTestCase(bench_op_obj, test_config)
