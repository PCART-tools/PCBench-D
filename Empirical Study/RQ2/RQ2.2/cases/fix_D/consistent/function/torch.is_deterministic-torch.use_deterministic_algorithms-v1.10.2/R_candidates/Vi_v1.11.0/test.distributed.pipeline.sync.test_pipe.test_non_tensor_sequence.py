def test_non_tensor_sequence(setup_rpc):
    class NonTensorTuple(nn.Module):
        def forward(self, x):
            return (x, "hello")

    class NonTensorArgs(nn.Module):
        def forward(self, x: str, y: bool):
            return x, y

    model = nn.Sequential(NonTensorTuple())
    model = Pipe(model)
    x = torch.rand(1)

    with pytest.raises(TypeError):
        model((x, "hello"))

    with pytest.raises(TypeError):
        model([x, "hello"])

    model = nn.Sequential(NonTensorArgs())
    model = Pipe(model)

    with pytest.raises(TypeError):
        # Need atleast one Tensor.
        model("hello", True)
