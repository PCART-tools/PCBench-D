@pytest.mark.parametrize("device", devices)
def test_serial_checkpoints(device):
    # Copied from https://github.com/pytorch/pytorch/pull/18568.
    timeline = []

    class Log(torch.autograd.Function):
        @staticmethod
        def forward(ctx, name, x):
            ctx.name = name
            timeline.append(f"{name}:forward")
            return x.detach()

        @staticmethod
        def backward(ctx, grad_output):
            name = ctx.name
            timeline.append(f"{name}:backward")
            return None, grad_output

    a = torch.rand(1, device=device, requires_grad=True)
    b = torch.rand(1, device=device, requires_grad=True)

    # Increase the next function sequence number.
    _ = a + 1 + 2 + 3 + 4 + 5

    a = checkpoint(partial(Log.apply, "a"), a)

    a, phony = fork(a)
    b = join(b, phony)

    b = checkpoint(partial(Log.apply, "b"), b)

    c = torch.cat((a, b))

    out = c.sum()

    #                        +--> {a} --Checkpoint(Log)--> {a}
    # {out} --Sum--> {c} --Cat     ^-----------------------------+
    #                        +--> {b} --Checkpoint(Log)--> {b} --First--> {b}
    out.backward()

    assert timeline == ["a:forward", "b:forward", "b:forward", "b:backward", "a:forward", "a:backward"]
