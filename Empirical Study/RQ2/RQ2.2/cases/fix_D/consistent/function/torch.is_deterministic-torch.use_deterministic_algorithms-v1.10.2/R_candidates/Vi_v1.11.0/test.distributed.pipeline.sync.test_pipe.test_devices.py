def test_devices(setup_rpc):
    a = nn.Linear(1, 1)
    b = nn.Linear(1, 1)
    c = nn.Linear(1, 1)

    # There are extra two devices.
    model = nn.Sequential(a, b, c)
    model = Pipe(model)

    cpu = torch.device("cpu")
    # Extra devices must be discarded.
    assert model.devices == [cpu, cpu, cpu]
