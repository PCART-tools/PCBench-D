@pytest.mark.parametrize("checkpoint", ["never", "always", "except_last"])
def test_no_tensor_output(checkpoint, setup_rpc):
    class Model1(nn.Module):
        def forward(self, a: int, b: Tensor, c: bool):
            return a, c, "hello"

    class Model2(nn.Module):
        def forward(self, a: int, b: bool, c: str):
            return a, c, b

    model = Pipe(nn.Sequential(Model1(), Model2()), chunks=5)
    a = random.randint(0, 10)
    b = torch.rand(10, 10)
    c = random.randint(0, 1) == 0

    # Need atleast one tensor across partitions too.
    with pytest.raises(TypeError):
        res = model(a, b, c).local_value()
