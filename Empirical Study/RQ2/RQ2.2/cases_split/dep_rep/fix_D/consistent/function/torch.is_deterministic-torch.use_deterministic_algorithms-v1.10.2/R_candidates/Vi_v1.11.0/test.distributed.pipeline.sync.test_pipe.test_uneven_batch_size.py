@pytest.mark.parametrize("checkpoint", ["never", "always", "except_last"])
def test_uneven_batch_size(checkpoint, setup_rpc):
    class Model(nn.Module):
        def forward(self, a: Tensor, b: int, c: Tensor):
            return a, b, c

    model = Pipe(nn.Sequential(Model()), checkpoint=checkpoint, chunks=5)
    a = torch.rand(3, 10)
    b = random.randint(0, 10)
    c = torch.rand(6, 10)
    res = model(a, b, c).local_value()
    assert torch.allclose(a, res[0])
    assert [b] * 3 == res[1]  # 3 chunks
    assert torch.allclose(c, res[2])

    # Two tensors producing uneven chunks would fail.
    model = Pipe(nn.Sequential(Model()), checkpoint=checkpoint, chunks=5)
    a = torch.rand(3, 10)
    b = random.randint(0, 10)
    c = torch.rand(4, 10)

    with pytest.raises(RuntimeError, match='Found different number of chunks'):
        model(a, b, c)
