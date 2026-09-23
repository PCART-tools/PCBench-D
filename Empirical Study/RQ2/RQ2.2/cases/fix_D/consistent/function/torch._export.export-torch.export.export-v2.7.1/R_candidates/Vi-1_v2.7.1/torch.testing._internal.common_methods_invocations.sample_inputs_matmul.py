def sample_inputs_matmul(op_info, device, dtype, requires_grad, is_rmatmul=False, **kwargs):
    make_arg = partial(make_tensor, dtype=dtype, device=device, low=None,
                       high=None, requires_grad=requires_grad)
    test_cases = (((L,), (L,)),
                  ((S, M), (M,)),
                  ((M,), (M, S)),
                  ((S, M), (M, S)),
                  ((S, 0), (0, M)),
                  ((S, S, M), (M,)),
                  ((S, S, M), (M, S)),
                  ((S, S, 0), (0, S)),
                  ((M,), (S, M, S)),
                  ((S, M), (S, M, S)),
                  ((0, 0), (S, 0, 0)),
                  ((S, S, M, M), (S, S, M, S)),
                  ((S, S, M, M), (M,)),
                  ((M,), (S, S, M, S)),
                  ((S, S, S), (1, S, S))
                  )
    for lhs_shape, rhs_shape in test_cases:
        lhs = make_arg(lhs_shape)
        rhs = make_arg(rhs_shape)
        if not is_rmatmul:
            yield SampleInput(lhs, rhs)
        else:
            yield SampleInput(rhs, lhs)
