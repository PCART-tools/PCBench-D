def test_concatenate_stack_dont_warn():
    with warnings.catch_warnings(record=True) as record:
        da.concatenate([da.ones(2, chunks=1)] * 62)
    assert not record

    with warnings.catch_warnings(record=True) as record:
        da.stack([da.ones(2, chunks=1)] * 62)
    assert not record
