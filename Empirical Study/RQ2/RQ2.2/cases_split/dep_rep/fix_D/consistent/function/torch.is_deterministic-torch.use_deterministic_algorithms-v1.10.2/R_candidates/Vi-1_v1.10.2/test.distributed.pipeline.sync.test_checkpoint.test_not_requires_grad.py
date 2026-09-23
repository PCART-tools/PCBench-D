def test_not_requires_grad():
    x = Batch(torch.rand(1, requires_grad=False))
    assert not x[0].requires_grad

    def f(x):
        return x * 2

    chk = Checkpointing(f, x)
    x = chk.checkpoint()
    assert x[0].requires_grad

    chk.recompute(x)
    assert x[0].requires_grad

    x.tensor.backward()
