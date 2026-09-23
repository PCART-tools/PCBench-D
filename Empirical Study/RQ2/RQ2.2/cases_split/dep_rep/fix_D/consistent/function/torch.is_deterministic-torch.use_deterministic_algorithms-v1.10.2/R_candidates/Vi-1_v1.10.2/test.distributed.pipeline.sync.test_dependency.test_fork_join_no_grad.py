def test_fork_join_no_grad(monkeypatch):
    def do_not_apply(*args):
        raise AssertionError("Function.apply called")

    monkeypatch.setattr("torch.autograd.Function.apply", do_not_apply)

    x = torch.rand(1, requires_grad=True)

    with torch.no_grad():
        x2, p = fork(x)

    assert not p.requires_grad
    assert x2 is x
    x = x2

    with torch.no_grad():
        x2 = join(x, p)

    assert x2 is x
    x = x2
