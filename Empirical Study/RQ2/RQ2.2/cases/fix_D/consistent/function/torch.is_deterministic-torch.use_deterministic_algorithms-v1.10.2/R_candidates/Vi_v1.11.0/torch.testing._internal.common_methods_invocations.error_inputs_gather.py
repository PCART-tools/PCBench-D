def error_inputs_gather(op_info, device, **kwargs):
    # src is [1, 2]
    #        [3, 4]
    src = torch.tensor(((1, 2), (3, 4)), device=device, dtype=torch.float32)

    # idx is [0, 0]
    #        [1, 0]
    idx = torch.tensor(((0, 0), (1, 0)), device=device, dtype=torch.long)

    # Index should be smaller than self except on dimesion 1
    bad_src = make_tensor((1, 1), device=device, dtype=torch.float32)
    yield ErrorInput(SampleInput(bad_src, args=(1, idx,)), error_type=RuntimeError,
                     error_regex="Size does not match at dimension 0")

    # Index must have long dtype
    bad_idx = idx.to(torch.int32)
    yield ErrorInput(SampleInput(src, args=(1, bad_idx)), error_type=RuntimeError,
                     error_regex="Expected dtype int64 for index")

    # TODO: FIXME
    # out.dtype must match src.dtype
    # Creates new src & idx since SampleInputs can't share tensors
    src = torch.tensor(((1, 2), (3, 4)), device=device, dtype=torch.float32)
    idx = torch.tensor(((0, 0), (1, 0)), device=device, dtype=torch.long)
    out = torch.empty((2, 2), device=device, dtype=torch.float64)
    yield ErrorInput(SampleInput(src, args=(1, idx), kwargs={'out': out}), error_type=RuntimeError,
                     error_regex="Expected out tensor to have dtype")

    # src and index tensors must have the same # of dimensions
    # idx too few dimensions
    src = torch.tensor(((1, 2), (3, 4)), device=device, dtype=torch.float32)
    idx = torch.tensor((0, 0), device=device, dtype=torch.long)
    yield ErrorInput(SampleInput(src, args=(1, idx)), error_type=RuntimeError,
                     error_regex="Index tensor must have the same number of dimensions")

    # src too few dimensions
    src = torch.tensor((1, 2), device=device, dtype=torch.float32)
    idx = torch.tensor(((0, 0), (1, 0)), device=device, dtype=torch.long)
    yield ErrorInput(SampleInput(src, args=(0, idx)), error_type=RuntimeError,
                     error_regex="Index tensor must have the same number of dimensions")

    # index out of bounds
    # NOTE: this ErrorInput is guarded because bounds checking does not occur on CUDA devices
    if torch.device(device).type == 'cpu':
        src = torch.tensor(((1, 2), (3, 4)), device=device, dtype=torch.float32)
        idx = torch.tensor(((0, 23), (1, 0)), device=device, dtype=torch.long)
        yield ErrorInput(SampleInput(src, args=(1, idx,)), error_type=RuntimeError,
                         error_regex="index 23 is out of bounds for dimension")
