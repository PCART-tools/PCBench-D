def wngrad_sparse_test_helper(parent_test, inputs, seq_b, lr, epsilon,
     engine, gc, dc):
    # helper functions for wngrad operator test
    param, grad = inputs
    seq_b = np.array([seq_b, ], dtype=np.float32)
    lr = np.array([lr], dtype=np.float32)

    # Create an indexing array containing values that are lists of indices,
    # which index into grad
    indices = np.random.choice(np.arange(grad.shape[0]),
        size=np.random.randint(grad.shape[0]), replace=False)

    # Sparsify grad
    grad = grad[indices]

    op = core.CreateOperator(
        "SparseWngrad",
        ["param", "seq_b", "indices", "grad", "lr"],
        ["param", "seq_b"],
        epsilon=epsilon,
        engine=engine,
        device_option=gc)

    def ref_sparse(param, seq_b, indices, grad, lr):
        param_out = np.copy(param)
        seq_b_out = np.copy(seq_b)
        seq_b_out = seq_b + 1.0 / seq_b * np.sum(grad * grad)
        for i, index in enumerate(indices):
            param_out[index] = param[index] + lr / (seq_b + epsilon) * grad[i]
        return (param_out, seq_b_out)

    logger.info('test_sparse_adagrad with full precision embedding')
    seq_b_i = seq_b.astype(np.float32)
    param_i = param.astype(np.float32)

    parent_test.assertReferenceChecks(
        gc, op, [param_i, seq_b_i, indices, grad, lr],
        ref_sparse
    )
