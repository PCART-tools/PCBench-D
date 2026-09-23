@pytest.mark.parametrize("checkpoint", ["never", "always", "except_last"])
def test_valid_non_tensor(checkpoint, setup_rpc):
    class NonTensor1(nn.Module):
        def forward(self, a: int, b: Tensor, c: bool, d: Tensor):
            res = b + a if c else b * a
            if d is not None:
                res += d
            return res, c, a, b, "hello", d

    class NonTensor2(nn.Module):
        def forward(self, a: Tensor, b: bool, c: int, d: Tensor, e: str, f: Tensor):
            res = a * c if b else a + c
            res += d
            return c, res, a, d + f if f is not None else d, b, e, f

    model = Pipe(nn.Sequential(NonTensor1(), NonTensor2()), chunks=5, checkpoint=checkpoint)
    a = random.randint(0, 10)
    b = torch.rand(10, 10)
    c = random.randint(0, 1) == 0
    d = torch.rand(10, 10)
    res = model(a, b, c, d).local_value()
    assert 7 == len(res)
    assert [a] * 5 == res[0]
    if c:
        assert torch.allclose(((b + a + d) * a) + b, res[1])
        assert torch.allclose(b + a + d, res[2])
    else:
        assert torch.allclose(((b * a) + d + a) + b, res[1])
        assert torch.allclose(b * a + d, res[2])
    assert torch.allclose(b + d, res[3])
    assert [c] * 5 == res[4]
    assert ["hello"] * 5 == res[5]
    assert torch.allclose(d, res[6])

    # Test one of the tensors can be None
    res = model(a, b, c, None).local_value()
    assert 7 == len(res)
    assert [a] * 5 == res[0]
    if c:
        assert torch.allclose(((b + a) * a) + b, res[1])
        assert torch.allclose(b + a, res[2])
    else:
        assert torch.allclose(((b * a) + a) + b, res[1])
        assert torch.allclose(b * a, res[2])
    assert torch.allclose(b, res[3])
    assert [c] * 5 == res[4]
    assert ["hello"] * 5 == res[5]
    assert [None] * 5 == res[6]

    # Need atleast one tensor.
    with pytest.raises(TypeError):
        model(a, None, c, None)
