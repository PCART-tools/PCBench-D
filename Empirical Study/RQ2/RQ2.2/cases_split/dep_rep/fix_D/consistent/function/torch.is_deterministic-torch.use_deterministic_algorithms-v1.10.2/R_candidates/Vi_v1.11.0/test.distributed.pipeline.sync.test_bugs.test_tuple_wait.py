@pytest.mark.skipif(torch.cuda.device_count() < 2, reason="2 cuda devices required")
def test_tuple_wait(cuda_sleep, setup_rpc):
    # In v0.0.3, Wait is applied to only the first tensor on a micro-batch.
    # Under this behavior, if checkpointing was disabled, there's a possibility
    # that gradient accumulations on other tensors are not synchronized
    # properly to the copy stream.
    class Sleep(torch.autograd.Function):
        @staticmethod
        def forward(ctx, x):
            return x.detach()

        @staticmethod
        def backward(ctx, grad):
            with torch.cuda.device(grad.device):
                cuda_sleep(0.05)
            return grad

    class Layer1(nn.Module):
        def __init__(self):
            super().__init__()
            self.ones = nn.Parameter(torch.ones(32, 3, 32, 32, requires_grad=True))

        def forward(self, a, b):
            a = a * self.ones
            return a * 1, b * 2, b * 3

    class Layer2(nn.Module):
        def __init__(self):
            super().__init__()
            self.ones = nn.Parameter(torch.ones(32, 3, 32, 32, requires_grad=True))

        def forward(self, a, b, c):
            a = a * self.ones
            b = Sleep.apply(b)
            return a + b + c

    model = nn.Sequential(Layer1().cuda(0), Layer2().cuda(1))
    model = Pipe(model, chunks=32, checkpoint="never")

    a = torch.rand(1024, 3, 32, 32, device=0, requires_grad=True)
    b = torch.rand(1024, 3, 32, 32, device=0, requires_grad=True)

    y = model(a, b)
    y.local_value().norm().backward()

    torch.cuda.synchronize(0)
    torch.cuda.synchronize(1)

    assert torch.isclose(b.grad.norm().cpu(), torch.tensor(5.000))
