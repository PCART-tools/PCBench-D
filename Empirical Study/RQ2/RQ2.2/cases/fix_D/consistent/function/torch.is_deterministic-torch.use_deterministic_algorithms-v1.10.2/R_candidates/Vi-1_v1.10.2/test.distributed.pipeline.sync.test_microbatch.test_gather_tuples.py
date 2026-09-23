def test_gather_tuples():
    a = (torch.zeros(1, 1), torch.zeros(2, 2))
    b = (torch.zeros(1, 1), torch.zeros(2, 2))

    ab = gather([Batch(a), Batch(b)])

    assert isinstance(ab, tuple)
    assert ab[0].size() == (2, 1)
    assert ab[1].size() == (4, 2)
