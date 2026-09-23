def test_atop_raises_on_incorrect_indices():
    x = da.arange(5, chunks=3)
    with pytest.raises(ValueError) as info:
        da.atop(lambda x: x, 'ii', x, 'ii', dtype=int)

    assert 'ii' in str(info.value)
    assert '1' in str(info.value)
