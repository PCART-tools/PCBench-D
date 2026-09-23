def test_input_singleton(setup_rpc):
    class One(nn.Module):
        def __init__(self):
            super().__init__()
            self.fc = nn.Linear(1, 1)

        def forward(self, a):
            return (self.fc(a),)

    model = nn.Sequential(One())
    model = Pipe(model, chunks=2)

    a = torch.rand(10, 1, requires_grad=True)

    (a_out,) = model(a).local_value()
    loss = a_out.mean()
    loss.backward()

    assert all(p.grad is not None for p in model.parameters())
    assert a.grad is not None
