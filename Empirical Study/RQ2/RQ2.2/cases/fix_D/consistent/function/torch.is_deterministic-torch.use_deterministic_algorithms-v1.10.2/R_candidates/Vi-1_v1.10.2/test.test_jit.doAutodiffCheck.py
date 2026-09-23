def doAutodiffCheck(testname):
    # TODO: setting false on test itself is not working
    if "test_t_" in testname or testname == "test_t":
        return False

    if GRAPH_EXECUTOR == ProfilingMode.SIMPLE:
        return False

    if GRAPH_EXECUTOR == ProfilingMode.LEGACY:
        return True


    # these tests are disabled because BailOut nodes
    # inserted by ProfilingExecutor interfere with
    # subgraph slicing of Differentiable Graphs
    test_exceptions = [
        # functional
        'test_nn_dropout',
        'test_nn_log_softmax',
        'test_nn_relu',
        'test_nn_softmax',
        'test_nn_threshold',
        'test_nn_lp_pool2d',
        'test_nn_lp_pool1d',
        'test_nn_gumbel_softmax_hard',
        'test_nn_gumbel_softmax',
        'test_nn_multilabel_soft_margin_loss',
        'test_nn_batch_norm',
        'test_nn_max_pool2d_with_indices',
        # AutogradJitGenerated
        'test___rdiv___constant',
        'test___rdiv___scalar_constant',
        'test_split',
        'test_split_dim',
        'test_split_dim_neg0',
        'test_split_size_list',
        'test_split_size_list_dim',
        'test_split_size_list_dim_neg0',
        'test_split_with_sizes',
        'test_split_with_sizes_dim',
        'test_split_with_sizes_dim_neg0',
        'test_split_with_sizes_size_0',
        'test_nn_max_pool2d_with_indices',
    ]

    if testname in test_exceptions:
        return False
    return True
