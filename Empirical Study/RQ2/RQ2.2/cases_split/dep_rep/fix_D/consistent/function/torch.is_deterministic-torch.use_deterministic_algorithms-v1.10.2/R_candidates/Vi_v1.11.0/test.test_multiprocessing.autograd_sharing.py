def autograd_sharing(queue, ready, master_modified, device, is_parameter):
    var = queue.get()
    ready.set()
    master_modified.wait()

    expected_var = torch.arange(1., 26, device=device).view(5, 5)
    expected_var[0, 0] = 1000
    is_ok = var.data.equal(expected_var)
    var.data[:] = torch.ones(5, 5, device=device)

    is_ok &= var.grad is None
    is_ok &= not var._backward_hooks
    if is_parameter:
        is_ok &= type(var) == Parameter
    else:
        is_ok &= type(var) == torch.Tensor
    var._grad = torch.ones(5, 5, device=device)

    queue.put(is_ok)
