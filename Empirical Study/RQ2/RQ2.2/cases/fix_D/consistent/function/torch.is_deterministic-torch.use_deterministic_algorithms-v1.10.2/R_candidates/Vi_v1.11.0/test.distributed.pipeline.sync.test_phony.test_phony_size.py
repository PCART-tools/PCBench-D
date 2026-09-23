def test_phony_size():
    p = get_phony(torch.device("cpu"), requires_grad=False)
    assert p.size() == (0,)
