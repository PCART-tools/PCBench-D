def test_phony_requires_grad():
    p1 = get_phony(torch.device("cpu"), requires_grad=True)
    p2 = get_phony(torch.device("cpu"), requires_grad=False)
    assert p1.requires_grad
    assert not p2.requires_grad
