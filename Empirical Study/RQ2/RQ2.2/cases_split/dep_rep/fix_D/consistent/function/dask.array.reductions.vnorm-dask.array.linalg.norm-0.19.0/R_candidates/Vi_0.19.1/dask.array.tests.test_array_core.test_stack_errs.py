def test_stack_errs():
    with pytest.raises(ValueError) as e:
        da.stack([da.zeros((2,), chunks=(2))] * 10 +
                 [da.zeros((3,), chunks=(3))] * 10)

    assert 'shape' in str(e.value).lower()
    assert '(2,)' in str(e.value)
    assert len(str(e.value)) < 105
