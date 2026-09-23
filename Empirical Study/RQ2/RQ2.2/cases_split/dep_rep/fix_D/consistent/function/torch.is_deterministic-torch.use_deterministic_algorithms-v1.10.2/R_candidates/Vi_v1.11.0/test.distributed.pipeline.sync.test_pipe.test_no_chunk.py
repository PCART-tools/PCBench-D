@pytest.mark.parametrize("checkpoint", ["never", "always", "except_last"])
def test_no_chunk(checkpoint, setup_rpc):
    class Model(nn.Module):
        def forward(self, a: Tensor, b: int, c: Tensor):
            return a, b, c

    model = Pipe(nn.Sequential(Model()), checkpoint=checkpoint, chunks=5)
    a = torch.rand(10, 10)
    b = random.randint(0, 10)
    c = torch.rand(10, 10)
    res = model(a, b, NoChunk(c)).local_value()
    assert torch.allclose(a, res[0])
    assert [b] * 5 == res[1]
    # c gets replicated due to NoChunk and the same tensor gets concatenated 5
    # times in the output.
    assert torch.allclose(torch.cat((c, c, c, c, c)), res[2])

    # Test invalid type for NoChunk
    with pytest.raises(TypeError, match='NoChunk only supported for tensors'):
        NoChunk(b)
