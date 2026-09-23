def test_fork_leak():
    leak = None

    class F(torch.autograd.Function):
        @staticmethod
        def forward(ctx, input):
            return input

        @staticmethod
        def backward(ctx, grad):
            nonlocal leak
            leak = weakref.ref(ctx)
            return grad

    x = torch.rand(1, requires_grad=True)
    x = F.apply(x)
    x, phony = fork(x)
    x = join(x, phony)

    x.backward()
    del x, phony

    assert leak() is None
