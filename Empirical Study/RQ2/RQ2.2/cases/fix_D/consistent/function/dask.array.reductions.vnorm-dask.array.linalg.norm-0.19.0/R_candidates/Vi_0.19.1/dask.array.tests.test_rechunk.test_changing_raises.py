def test_changing_raises():
    nan = float('nan')
    with pytest.raises(ValueError) as record:
        _old_to_new(((nan, nan), (4, 4)), ((nan, nan, nan), (4, 4)))

    assert 'unchanging' in str(record.value)
