def test_parallel_randoms(setup_rpc):
    class Dropouts(nn.Module):
        def forward(self, x):
            for _ in range(100):
                x = F.dropout(x, p=0.001)
            return x

    model = nn.Sequential(Dropouts(), Dropouts())

    x = torch.rand(10, 10, requires_grad=True)
    model = Pipe(model, chunks=10, checkpoint="always")
    y = model(x)
    y = y.local_value()
    y.norm().backward()

    assert y.to(torch.bool).tolist() == x.grad.to(torch.bool).tolist()
