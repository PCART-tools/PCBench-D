def test_input_pair(setup_rpc):
    class Two(nn.Module):
        def __init__(self):
            super().__init__()
            self.fc_a = nn.Linear(1, 1)
            self.fc_b = nn.Linear(1, 1)

        def forward(self, a, b):
            return (self.fc_a(a), self.fc_b(b))

    model = nn.Sequential(Two())
    model = Pipe(model, chunks=2)

    a = torch.rand(10, 1, requires_grad=True)
    b = torch.rand(10, 1, requires_grad=True)

    a_out, b_out = model(a, b).local_value()
    loss = (a_out + b_out).mean()
    loss.backward()

    assert a.grad is not None
    assert b.grad is not None
