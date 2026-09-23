def test_concatenate_errs():
    with pytest.raises(ValueError) as e:
        da.concatenate([da.zeros((2, 1), chunks=(2, 1)),
                        da.zeros((2, 3), chunks=(2, 3))])

    assert 'shape' in str(e).lower()
    assert '(2, 1)' in str(e)

    with pytest.raises(ValueError):
        da.concatenate([da.zeros((1, 2), chunks=(1, 2)),
                        da.zeros((3, 2), chunks=(3, 2))], axis=1)
