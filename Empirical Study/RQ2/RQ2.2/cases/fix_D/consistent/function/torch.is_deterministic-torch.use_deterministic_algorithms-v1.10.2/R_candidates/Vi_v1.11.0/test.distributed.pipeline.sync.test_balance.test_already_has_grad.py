def test_already_has_grad():
    model = nn.Sequential(nn.Conv2d(3, 3, 1))
    sample = torch.rand(1, 3, 32, 32)
    model(sample).norm().backward()

    with pytest.raises(ValueError, match="some parameter already has gradient"):
        balance_by_time(1, model, sample, device="cpu")
