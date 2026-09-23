def test_not_requires_grad_with_parameter():
    x = torch.rand(1, requires_grad=False)
    a = torch.rand(1, requires_grad=True)

    def f(x):
        return x * a

    y = checkpoint(f, x)
    y.backward()

    assert a.grad is not None
