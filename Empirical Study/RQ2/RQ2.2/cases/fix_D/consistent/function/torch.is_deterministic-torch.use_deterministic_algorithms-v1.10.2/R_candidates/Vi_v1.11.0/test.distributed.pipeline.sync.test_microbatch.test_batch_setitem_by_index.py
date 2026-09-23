def test_batch_setitem_by_index():
    a = Batch(torch.tensor(42))
    b = Batch((torch.tensor(42), torch.tensor(21)))

    a[0] = torch.tensor(0)
    b[0] = torch.tensor(0)

    assert a.atomic
    assert a[0].item() == 0

    assert not b.atomic
    assert len(b) == 2
    assert b[0].item() == 0
    assert b[1].item() == 21
