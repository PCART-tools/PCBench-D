def test_fork_join_enable_grad():
    x = torch.rand(1, requires_grad=True)

    with torch.enable_grad():
        x2, p = fork(x)

    assert p.requires_grad
    assert x2 is not x
    x = x2

    assert x.requires_grad
    assert p.requires_grad
    assert x.grad_fn.__class__ is Fork._backward_cls
    assert p.grad_fn.__class__ is Fork._backward_cls

    with torch.enable_grad():
        x2 = join(x, p)

    assert x2 is not x
    x = x2

    assert x.requires_grad
    assert x.grad_fn.__class__ is Join._backward_cls
