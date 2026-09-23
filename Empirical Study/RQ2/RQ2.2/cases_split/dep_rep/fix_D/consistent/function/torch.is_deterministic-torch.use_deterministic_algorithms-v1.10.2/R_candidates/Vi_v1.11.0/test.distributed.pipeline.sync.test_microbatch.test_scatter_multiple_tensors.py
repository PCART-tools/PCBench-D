def test_scatter_multiple_tensors():
    ab = (torch.zeros(2, 1), torch.zeros(4, 2))

    a, b = scatter(*ab, chunks=2)

    assert list(a)[0].size() == (1, 1)
    assert list(b)[0].size() == (1, 1)
    assert list(a)[1].size() == (2, 2)
    assert list(b)[1].size() == (2, 2)
