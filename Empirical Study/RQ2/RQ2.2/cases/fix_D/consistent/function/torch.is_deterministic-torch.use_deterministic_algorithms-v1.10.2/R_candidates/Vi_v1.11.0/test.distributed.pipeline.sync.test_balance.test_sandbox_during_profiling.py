@pytest.mark.parametrize("device", devices)
def test_sandbox_during_profiling(device):
    model = nn.Sequential(nn.BatchNorm2d(3))

    before = {k: v.clone() for k, v in model.state_dict().items()}

    sample = torch.rand(1, 3, 10, 10)
    balance_by_time(1, model, sample, device=device)

    after = model.state_dict()

    assert before.keys() == after.keys()
    for key, value in before.items():
        assert torch.allclose(after[key], value), key
