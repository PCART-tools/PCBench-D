def test_scatter_tensor():
    ab = torch.zeros(2, 1)

    a, b = scatter(ab, chunks=2)

    assert a.tensor.size() == (1, 1)
    assert b.tensor.size() == (1, 1)
