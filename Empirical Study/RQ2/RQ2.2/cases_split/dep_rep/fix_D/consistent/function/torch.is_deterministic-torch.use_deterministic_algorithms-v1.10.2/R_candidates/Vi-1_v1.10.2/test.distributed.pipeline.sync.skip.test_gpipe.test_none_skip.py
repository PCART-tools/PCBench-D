def test_none_skip(setup_rpc):
    @skippable(stash=["none"])
    class Stash(nn.Module):
        def forward(self, input):
            yield stash("none", None)
            return input  # noqa: B901

    @skippable(pop=["none"])
    class Pop(nn.Module):
        def forward(self, input):
            none = yield pop("none")
            assert none is None
            return input

    model = nn.Sequential(Stash(), Pop())
    model = Pipe(model, chunks=5)

    input = torch.rand(10, requires_grad=True)
    output = model(input)

    def assert_grad_fn_is_not_portal(grad_fn, visited=None):
        if visited is None:
            visited = set()
        if grad_fn in visited or grad_fn is None:
            return

        assert not isinstance(grad_fn, PortalBlue._backward_cls)
        assert not isinstance(grad_fn, PortalCopy._backward_cls)
        assert not isinstance(grad_fn, PortalOrange._backward_cls)

        visited.add(grad_fn)
        for next_grad_fn, _ in grad_fn.next_functions:
            assert_grad_fn_is_not_portal(next_grad_fn, visited)

    assert_grad_fn_is_not_portal(output.local_value().grad_fn)

    output.local_value().sum().backward()
    assert input.grad.mean().item() == 1
