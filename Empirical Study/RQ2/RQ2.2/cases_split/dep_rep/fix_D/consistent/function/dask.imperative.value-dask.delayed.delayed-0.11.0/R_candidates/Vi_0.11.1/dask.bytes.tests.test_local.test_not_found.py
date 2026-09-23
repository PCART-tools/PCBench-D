def test_not_found():
    fn = 'not-a-file'
    with pytest.raises(FileNotFoundError) as e:
        read_bytes(fn)
    assert fn in str(e)
