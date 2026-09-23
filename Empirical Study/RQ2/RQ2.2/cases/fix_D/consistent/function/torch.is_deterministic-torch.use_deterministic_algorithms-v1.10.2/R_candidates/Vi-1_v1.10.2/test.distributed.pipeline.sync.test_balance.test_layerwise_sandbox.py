@pytest.mark.parametrize("device", devices)
def test_layerwise_sandbox(device):
    model = nn.Sequential(nn.Conv2d(3, 3, 1), nn.BatchNorm2d(3))
    model.eval()

    for layer in layerwise_sandbox(model, torch.device(device)):
        assert layer.training
        assert all(p.device.type == device for p in layer.parameters())

    assert all(not l.training for l in model)
    assert all(p.device.type == "cpu" for p in model.parameters())
