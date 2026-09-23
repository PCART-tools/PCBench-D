def sample_inputs_comparison_ops(self, device, dtype, requires_grad, **kwargs):
    test_cases = (
        ((S, S, S), (S, S, S), False),
        ((S, S, S), (), False),
        ((S, S, S), (1,), False),
        ((S,), (1,), False),
        ((), (), False),
    )
    test_cases_lhs_broadcasting = (
        ((S, 1, S), (S, S, S), True),
        ((1,), (S, S, S), True),
        ((1, S), (1, 1, S), True),
        ((), (0,), True),
        ((), (S, S, S), True),
    )
    cases = test_cases + test_cases_lhs_broadcasting
    sample_inputs = list(SampleInput(make_tensor(first_shape, device, dtype,
                                                 requires_grad=requires_grad),
                                     args=(make_tensor(second_shape, device, dtype,
                                                       requires_grad=requires_grad),),
                                     broadcasts_input=broadcasts_input)
                         for first_shape, second_shape, broadcasts_input in cases)
    equal_tensors_non_bool = (
        ([[[-8, 6], [9, 0]], [[0, 5], [5, 7]]]),
        ([[[6, 5]], [[1, -5]]]),
        ([[2], [-1]]),
        ([0, -6]),
        ([3],),
    )
    equal_tensors_bool = (
        ([[[1, 0], [0, 0]], [[0, 1], [1, 0]]]),
        ([[[1, 1]], [[1, 0]]]),
        ([[1], [0]]),
        ([0, 1]),
        ([1],),
    )
    more_cases = equal_tensors_bool if dtype is torch.bool else equal_tensors_non_bool
    more_inputs = list(SampleInput(torch.tensor(elements, device=device, dtype=dtype,
                                                requires_grad=requires_grad),
                                   args=(torch.tensor(elements, device=device, dtype=dtype,
                                                      requires_grad=requires_grad),))
                       for elements in more_cases)
    sample_inputs = [*sample_inputs, *more_inputs]
    return tuple(sample_inputs)
