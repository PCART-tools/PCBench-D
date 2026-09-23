def test_non_tensor(setup_rpc):
    class NonTensor(nn.Module):
        def forward(self, _):
            return "hello"

    model = nn.Sequential(NonTensor())
    model = Pipe(model)
    x = torch.rand(1)

    with pytest.raises(TypeError):
        model(x)

    with pytest.raises(TypeError):
        model("hello")
