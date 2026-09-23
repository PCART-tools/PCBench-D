def sample_inputs_index_put(
    op_info, device, dtype, requires_grad, op_kwargs=None, **kwargs
):
    for njt in _sample_njts(
        device=device, dtype=dtype, requires_grad=requires_grad, dims=[2, 3, 4]
    ):
        for dim in range(njt.dim()):
            indices = [
                torch.tensor(list(range(njt.size(0))), device=njt.device),
                *[
                    torch.tensor([0] * njt.size(0), device=njt.device)
                    for _ in range(dim - 1)
                ],
            ]
            njt_desc = _describe_njt(njt)
            yield SampleInput(
                _clone(njt),
                kwargs={
                    "indices": indices,
                    "values": torch.tensor(1.0, device=njt.device),
                },
                name=f"{njt_desc}: up to dim {dim - 1}",
            )

    # Non-cont NJT for completeness
    offsets = torch.tensor([0, 2, 5, 7], device=device)
    lengths = torch.tensor([2, 2, 2], device=device)
    indices = [
        torch.tensor([0, 1, 2], device=device),
        torch.tensor([0, 1, 1], device=device),
        torch.tensor([0, 0, 0], device=device),
    ]
    a = torch.nested.nested_tensor_from_jagged(
        torch.zeros(7, 3, device=device), offsets, lengths
    ).requires_grad_(requires_grad)

    njt_desc = _describe_njt(a)
    yield SampleInput(
        _clone(a),
        kwargs={"indices": indices, "values": torch.tensor(1.0, device=a.device)},
        name=f"{njt_desc}: all dims",
    )
