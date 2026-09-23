def sample_inputs_searchsorted(op_info, device, dtype, requires_grad, **kwargs):
    make_arg = partial(make_tensor, dtype=dtype, device=device, requires_grad=requires_grad)

    sizes = ((0,), (M,), (0, 0), (M, M), (0, 0, 0), (M, M, M))
    inputs = []
    for size, noncontiguous, out_int32, right in product(sizes, [False, True], [False, True], [False, True]):
        unsorted_tensor = make_arg(size, noncontiguous=noncontiguous)
        input_tensor = make_arg(size, noncontiguous=noncontiguous)
        if np.product(size) == 0:
            boundary_tensor = unsorted_tensor
            sorter = make_tensor(size, dtype=torch.int64, device=device, noncontiguous=noncontiguous)
        else:
            boundary_tensor, sorter = torch.sort(unsorted_tensor)
        side = "right" if right else "left"

        inputs.append(SampleInput(boundary_tensor, args=(input_tensor,), kwargs=dict(out_int32=out_int32, right=right)))
        inputs.append(SampleInput(boundary_tensor, args=(input_tensor,), kwargs=dict(out_int32=out_int32, side=side)))

        inputs.append(
            SampleInput(unsorted_tensor, args=(input_tensor,), kwargs=dict(out_int32=out_int32, right=right, sorter=sorter)))
        inputs.append(
            SampleInput(unsorted_tensor, args=(input_tensor,), kwargs=dict(out_int32=out_int32, side=side, sorter=sorter)))
    return inputs
