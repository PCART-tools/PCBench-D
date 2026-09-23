def test_join_when_fork_not_requires_grad():
    x = torch.rand(2, 1)
    a, b = x.chunk(2)

    assert not a.requires_grad
    a, p = fork(a)
    assert not a.requires_grad
    assert not p.requires_grad

    assert not b.requires_grad
    b = join(b, p)
    assert not b.requires_grad
