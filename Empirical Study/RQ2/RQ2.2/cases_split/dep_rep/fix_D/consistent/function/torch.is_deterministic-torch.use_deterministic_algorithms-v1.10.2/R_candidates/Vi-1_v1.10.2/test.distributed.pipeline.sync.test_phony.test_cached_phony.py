def test_cached_phony():
    p1 = get_phony(torch.device("cpu"), requires_grad=True)
    p2 = get_phony(torch.device("cpu"), requires_grad=True)
    assert p1 is p2

    p3 = get_phony(torch.device("cpu"), requires_grad=False)
    p4 = get_phony(torch.device("cpu"), requires_grad=False)
    assert p3 is p4

    assert p1 is not p3
