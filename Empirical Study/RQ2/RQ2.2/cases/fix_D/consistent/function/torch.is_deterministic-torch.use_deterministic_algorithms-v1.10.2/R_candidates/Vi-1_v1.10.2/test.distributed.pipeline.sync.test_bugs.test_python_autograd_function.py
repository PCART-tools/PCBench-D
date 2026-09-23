def test_python_autograd_function(setup_rpc):
    # A Python autograd function might fail with this error:
    #
    #   RuntimeError: Returning Variables sharing storage with other Variables
    #   that require grad is not supported in Python functions. Please submit a
    #   feature request if you hit this error.
    #
    # It doesn't look like an essential restriction. But it happens on the
    # current PyTorch version. To avoid it, we should detach the tensor before
    # returning by identity autograd functions, such as Wait, Fork, and Join.
    #
    class Identity(torch.autograd.Function):
        @staticmethod
        def forward(ctx, input):
            return input

        @staticmethod
        def backward(ctx, grad):
            return grad

    class M(nn.Module):
        def forward(self, input):
            return Identity.apply(input)

    model = nn.Sequential(M(), M())
    model = Pipe(model, checkpoint="always")

    x = torch.rand(42)
    y = model(x)
    assert torch.allclose(x, y.local_value())
