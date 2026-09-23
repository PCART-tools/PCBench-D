def sample_inputs_householder_product(op_info, device, dtype, requires_grad, **kwargs):
    """
    This function generates input for torch.linalg.householder_product (torch.orgqr).
    The first argument should be a square matrix or batch of square matrices, the second argument is a vector or batch of vectors.
    Empty, square, rectangular, batched square and batched rectangular input is generated.
    """
    # Each column of the matrix is getting multiplied many times leading to very large values for
    # the Jacobian matrix entries and making the finite-difference result of grad check less accurate.
    # That's why gradcheck with the default range [-9, 9] fails and [-2, 2] is used here.
    samples = (
        SampleInput(make_tensor((S, S), device, dtype, low=-2, high=2, requires_grad=requires_grad),
                    args=(make_tensor((S,), device, dtype, low=-2, high=2, requires_grad=requires_grad),)),

        SampleInput(make_tensor((S + 1, S), device, dtype, low=-2, high=2, requires_grad=requires_grad),
                    args=(make_tensor((S,), device, dtype, low=-2, high=2, requires_grad=requires_grad),)),

        SampleInput(make_tensor((2, 1, S, S), device, dtype, low=-2, high=2, requires_grad=requires_grad),
                    args=(make_tensor((2, 1, S,), device, dtype, low=-2, high=2, requires_grad=requires_grad),)),

        SampleInput(make_tensor((2, 1, S + 1, S), device, dtype, low=-2, high=2, requires_grad=requires_grad),
                    args=(make_tensor((2, 1, S,), device, dtype, low=-2, high=2, requires_grad=requires_grad),)),

        SampleInput(make_tensor((0, 0), device, dtype, low=None, high=None, requires_grad=requires_grad),
                    args=(make_tensor((0,), device, dtype, low=None, high=None, requires_grad=requires_grad),)),

        SampleInput(make_tensor((S, S), device, dtype, low=-2, high=2, requires_grad=requires_grad),
                    args=(make_tensor((0,), device, dtype, low=None, high=None, requires_grad=requires_grad),)),
    )

    return samples
