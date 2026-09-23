def test_batch_atomic():
    x = torch.tensor(42)
    b = Batch(x)

    assert b.atomic

    assert b.tensor is x
    with pytest.raises(AttributeError):
        b.tensors

    assert list(b) == [x]
    assert len(b) == 1
    assert b[0] is x
