def sample_inputs_matmul(op_info, device, dtype, requires_grad):
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
                  ((M,), (S, S, M, S)))
    sample_inputs = []
    for lhs_shape, rhs_shape in test_cases:
        lhs = make_tensor(lhs_shape, device, dtype, low=None, high=None, requires_grad=requires_grad)
        rhs = make_tensor(rhs_shape, device, dtype, low=None, high=None, requires_grad=requires_grad)
        if op_info.name == 'matmul':
            sample_inputs.append(SampleInput(lhs, args=(rhs,)))
        elif op_info.name == '__rmatmul__':
            sample_inputs.append(SampleInput(rhs, args=(lhs,)))
        else:
            raise RuntimeError("`op_info.name` must be 'matmul' or '__rmatmul__'")
    return tuple(sample_inputs)
