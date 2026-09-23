def test_gather_tensors():
    a = torch.zeros(1, 1)
    b = torch.zeros(1, 1)

    ab = gather([Batch(a), Batch(b)])

    assert ab.size() == (2, 1)
