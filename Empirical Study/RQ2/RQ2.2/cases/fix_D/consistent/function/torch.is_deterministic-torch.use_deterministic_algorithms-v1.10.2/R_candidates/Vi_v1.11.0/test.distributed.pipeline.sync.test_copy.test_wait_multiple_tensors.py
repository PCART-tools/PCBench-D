def test_wait_multiple_tensors():
    a = torch.rand(1, requires_grad=True)
    b = torch.rand(1, requires_grad=True)

    a, b = Wait.apply(CPUStream, CPUStream, a, b)

    assert a.grad_fn is b.grad_fn
    assert a.grad_fn.__class__ is Wait._backward_cls
