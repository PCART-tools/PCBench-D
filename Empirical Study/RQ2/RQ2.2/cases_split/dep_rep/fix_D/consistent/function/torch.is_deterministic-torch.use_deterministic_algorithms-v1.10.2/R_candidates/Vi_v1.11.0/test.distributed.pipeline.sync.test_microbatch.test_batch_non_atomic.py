def test_batch_non_atomic():
    x, y = torch.tensor(42), torch.tensor(21)
    b = Batch((x, y))

    assert not b.atomic

    with pytest.raises(AttributeError):
        b.tensor

    assert list(b) == [x, y]
    assert len(b) == 2
    assert b[0] is x
    assert b[1] is y
