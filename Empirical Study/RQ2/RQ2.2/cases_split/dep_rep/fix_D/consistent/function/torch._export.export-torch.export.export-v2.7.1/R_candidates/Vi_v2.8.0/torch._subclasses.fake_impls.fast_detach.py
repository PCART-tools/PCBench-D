def fast_detach(fake_mode, x, include_real=False):
    with no_python_dispatcher(), in_kernel_invocation_manager(fake_mode):
        out = torch.ops.aten.detach.default(x)
    if include_real:
        return FakeTensor(fake_mode, out, x.device, real_tensor=x.real_tensor)
    return FakeTensor(fake_mode, out, x.device)
