def test_phony_in_autograd_function():
    class Phonify(torch.autograd.Function):
        @staticmethod
        def forward(ctx, input):
            phony = get_phony(input.device, requires_grad=False)
            return phony.detach()

    x = torch.rand(1, requires_grad=True)

    p1 = Phonify.apply(x)
    p2 = get_phony(torch.device("cpu"), requires_grad=True)

    assert p1 is not p2
    assert p1.grad_fn is not None
    assert p2.grad_fn is None
