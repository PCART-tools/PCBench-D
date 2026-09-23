def _test_copy_wait(prev_stream, next_stream, cuda_sleep=None):
    device = get_device(prev_stream)

    with use_stream(prev_stream):
        if is_cuda(prev_stream):
            cuda_sleep(0.5)
        x = torch.ones(100, device=device, requires_grad=True)

    (y,) = Copy.apply(prev_stream, next_stream, x)
    (y,) = Wait.apply(prev_stream, next_stream, x)

    with use_stream(next_stream):
        assert torch.allclose(y.sum(), torch.tensor(100.0, device=device))
        y.norm().backward()
    with use_stream(prev_stream):
        assert torch.allclose(x.grad.sum(), torch.tensor(10.0, device=device))
