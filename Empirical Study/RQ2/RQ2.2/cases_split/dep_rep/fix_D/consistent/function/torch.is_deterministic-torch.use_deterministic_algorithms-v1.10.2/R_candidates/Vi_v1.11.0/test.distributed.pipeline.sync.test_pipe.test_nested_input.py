def test_nested_input(setup_rpc):
    class NestedInput(nn.Module):
        def __init__(self):
            super().__init__()
            self.fc_a = nn.Linear(1, 1)
            self.fc_b = nn.Linear(1, 1)

        def forward(self, inp):
            return inp

    model = nn.Sequential(NestedInput())
    model = Pipe(model, chunks=2)

    a = torch.rand(10, 1, requires_grad=True)
    b = torch.rand(10, 1, requires_grad=True)

    # TypeError: expected Tensor, but got tuple
    with pytest.raises(TypeError):
        model((a, (a, b))).local_value()

    # TypeError: expected Tensor, but got list
    with pytest.raises(TypeError):
        model((a, [a, b])).local_value()
