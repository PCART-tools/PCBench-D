@pytest.mark.skipif(not torch.cuda.is_available(), reason="cuda required")
def test_fork_join():
    logs = []

    class Log(torch.autograd.Function):
        @staticmethod
        def forward(ctx, number, tensor):
            ctx.number = number
            return tensor.detach()

        @staticmethod
        def backward(ctx, grad):
            logs.append(ctx.number)
            return None, grad

    a = torch.rand(1, device="cpu", requires_grad=True)
    b = torch.rand(1, device="cuda", requires_grad=True)

    a = Log.apply(1, a)

    a, phony = fork(a)
    b = join(a, phony)

    b = Log.apply(2, b)
    b = b.to("cpu")

    (a + b).backward()

    assert logs == [2, 1]
