def sample_inputs_index_select(op_info, device, dtype, requires_grad):
    return (
        SampleInput(
            make_tensor((S, S, S), device, dtype, low=None, high=None, requires_grad=requires_grad),
            args=(0, index_variable(2, S, device=device))),
        SampleInput(
            make_tensor((), device, dtype, low=None, high=None, requires_grad=requires_grad),
            args=(0, torch.tensor([0], dtype=torch.int64, device=device))),
        SampleInput(
            make_tensor((), device, dtype, low=None, high=None, requires_grad=requires_grad),
            args=(0, torch.tensor(0, dtype=torch.int64, device=device))),
    )
