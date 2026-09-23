def test_join_when_fork_requires_grad():
    x = torch.rand(2, 1)
    a, b = x.chunk(2)

    a.requires_grad_()
    assert a.requires_grad
    a, p = fork(a)
    assert a.requires_grad
    assert p.requires_grad

    assert not b.requires_grad
    b = join(b, p)
    assert b.requires_grad
