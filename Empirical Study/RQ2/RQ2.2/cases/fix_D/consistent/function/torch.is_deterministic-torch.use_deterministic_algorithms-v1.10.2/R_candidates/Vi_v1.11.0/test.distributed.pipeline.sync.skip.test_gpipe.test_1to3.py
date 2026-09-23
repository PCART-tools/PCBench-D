@pytest.mark.skipif(not torch.cuda.is_available(), reason="cuda required")
@pytest.mark.parametrize("balance", [[3], [1, 2], [2, 1], [1, 1, 1]], ids=["3", "1:2", "2:1", "1:1:1"])
@pytest.mark.parametrize("checkpoint", ["never", "always", "except_last"])
def test_1to3(balance, checkpoint, setup_rpc):
    if torch.cuda.device_count() < len(balance):
        pytest.skip("at least %d cuda devices required" % len(balance))

    @skippable(stash=["1to3"])
    class Layer1(nn.Module):
        def __init__(self):
            super().__init__()
            self.conv = nn.Conv2d(3, 3, 1)

        def forward(self, input):
            yield stash("1to3", input)
            output = self.conv(input)
            return output  # noqa: B901

    class Layer2(nn.Module):
        def __init__(self):
            super().__init__()
            self.conv = nn.Conv2d(3, 3, 1)

        def forward(self, input):
            output = self.conv(input)
            return output

    @skippable(pop=["1to3"])
    class Layer3(nn.Module):
        def __init__(self):
            super().__init__()
            self.conv = nn.Conv2d(3, 3, 1)

        def forward(self, input):
            skip_1to3 = yield pop("1to3")
            output = self.conv(input) + skip_1to3
            return output

    model = nn.Sequential(Layer1(), Layer2(), Layer3())
    model = partition_model(model, balance)
    model = Pipe(model, chunks=3, checkpoint=checkpoint)

    in_device = model.devices[0]
    out_device = model.devices[-1]

    input = torch.rand(30, 3, 224, 224, device=in_device, requires_grad=True)
    output = model(input)
    loss = output.local_value().mean()
    loss.backward()

    assert torch.allclose(output.local_value().norm(), torch.tensor(1039.0, device=out_device), atol=6e-1)
    assert torch.allclose(input.grad.norm(), torch.tensor(0.0004533053, device=in_device))
