def _get_grad_blob(grad_map, input_to_check):
    grad_blob = grad_map[input_to_check]

    if isinstance(grad_blob, core.BlobReference):
        return workspace.blobs[grad_blob]

    # If grad_blob is not a single blob, it should be a gradient slice.
    # To make it comparable with the estimiated gradient which is dense,
    # we need to first convert grad_blob to dense gradient.
    assert isinstance(grad_blob, core.GradientSlice)
    dense_grad = 'tmp_dense_grad'
    sparse_to_dense_op = core.CreateOperator(
        'SparseToDense',
        [grad_blob.indices, grad_blob.values, input_to_check],
        dense_grad,
    )
    workspace.RunOperatorOnce(sparse_to_dense_op)
    return workspace.blobs[dense_grad]
