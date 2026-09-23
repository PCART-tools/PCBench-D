def generate_c2_test_from_ops(ops_metadata, bench_op, tags):
    """
    This function is used to generate Caffe2 tests based on the metadata
    of operators. The metadata includes seven fields which are 1) op_type:
    the name of the operator. 2) num_inputs: the number of input blobs.
    3) input_dims: a dictionary which includes the shapes of the input blobs.
    4) input_types: a list which includes the types of input blobs. 5)
    output_dims: a dictionary which includes the shapes of output blobs.
    6) num_oupts: the number of output blobs. 7) args: a dictionary which
    includes the args for th operator.
    Here is an example to show the metadata for the WeighedSum operator
    op_type : WeightedSum
    num_inputs: 4
    input_dims: {'0': [256], '1': [1], '2': [256], '3': [1]}
    input_types: ['float', 'float', 'float', 'float']
    output_dims:  {'0': [256]}
    num_outputs: 4
    args: {}
    TODO(mingzhe0908): introduce device and add it to the benchmark name
    """
    for op_metadata in ops_metadata:
        tmp_attrs = OpMeta(op_metadata.op_type,
                           op_metadata.num_inputs,
                           op_metadata.input_dims,
                           op_metadata.input_types,
                           op_metadata.output_dims,
                           op_metadata.num_outputs,
                           op_metadata.args,
                           op_metadata.device)
        test_attrs = tmp_attrs._asdict()
        op = bench_op()
        op.init(**test_attrs)
        test_name = op.test_name("short")
        input_config = "Shapes: {}, Type: {}, Args: {}".format(
            op_metadata.input_dims,
            op_metadata.input_types,
            str(op_metadata.args))
        test_config = TestConfig(test_name, input_config, tags, run_backward=False)
        if op is not None:
            create_caffe2_op_test_case(
                op,
                test_config)
