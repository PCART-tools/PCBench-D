def sample_inputs_gradient(op_info, device, dtype, requires_grad):
    sample_inputs = []
    test_cases_float = (
        ((S,), None, None, 1),
        ((S,), 2., None, 1),
        ((S, S), None, None, 2),
        ((S, S), [2.0, 2.1], None, 1),
        ((S, S), [2.0, 2.1], (0, 1), 1),
        ((4, 4, 4), [2., 1.], (0, 1), 2),
    )
    for size, spacing, dim, edge_order in test_cases_float:
        t = make_tensor(size, device, dtype, low=None, high=None, requires_grad=requires_grad)
        sample_inputs.append(SampleInput(t, kwargs=dict(dim=dim, spacing=spacing, edge_order=edge_order)))

    test_cases_tensor = (
        ((3, 3, 3), ((1.1, 2.0, 3.5), (4.0, 2, 6.0)), (0, -1), 1),
        ((3, 3, 3), ((1.0, 3.0, 2.0), (8.0, 6.0, 1.0)), (0, 1), 2),
    )
    for size, coordinates, dim, edge_order in test_cases_tensor:
        t = make_tensor(size, device, dtype, low=None, high=None, requires_grad=requires_grad)
        coordinates_tensor_list = []
        for coords in coordinates:
            a = torch.tensor(coords, dtype=dtype, device=device)
            coordinates_tensor_list.append(a)
        sample_inputs.append(SampleInput(t, kwargs=dict(dim=dim, spacing=coordinates_tensor_list, edge_order=edge_order)))

    return tuple(sample_inputs)
