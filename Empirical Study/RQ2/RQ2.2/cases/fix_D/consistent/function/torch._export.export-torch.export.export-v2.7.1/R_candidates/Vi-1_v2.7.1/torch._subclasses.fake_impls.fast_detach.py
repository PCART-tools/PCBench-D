def fast_detach(fake_mode, x):
    with no_python_dispatcher(), in_kernel_invocation_manager(fake_mode):
        out = torch.ops.aten.detach.default(x)
    return FakeTensor(fake_mode, out, x.device)
