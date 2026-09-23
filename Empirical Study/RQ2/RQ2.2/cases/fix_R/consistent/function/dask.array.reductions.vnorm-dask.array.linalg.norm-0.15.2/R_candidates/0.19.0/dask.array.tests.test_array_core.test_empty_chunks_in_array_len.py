def test_empty_chunks_in_array_len():
    x = da.ones((), chunks=())
    with pytest.raises(TypeError) as exc_info:
        len(x)

    err_msg = 'len() of unsized object'
    assert err_msg in str(exc_info.value)
