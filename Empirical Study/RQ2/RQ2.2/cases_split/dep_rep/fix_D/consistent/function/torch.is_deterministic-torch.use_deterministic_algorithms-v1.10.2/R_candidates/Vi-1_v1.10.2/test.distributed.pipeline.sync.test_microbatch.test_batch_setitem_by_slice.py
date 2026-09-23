def test_batch_setitem_by_slice():
    a = Batch(torch.tensor(42))
    b = Batch((torch.tensor(42), torch.tensor(21)))

    a[:] = (torch.tensor(0),)
    b[:] = (torch.tensor(0),)

    assert a.atomic
    assert a[0].item() == 0

    assert not b.atomic
    assert len(b) == 1
    assert b[0].item() == 0
