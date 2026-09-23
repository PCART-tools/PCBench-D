@pytest.mark.parametrize('fmt', list(seekable_files))
def test_getsize(fmt):
    with s3_context('compress', {'x': compress[fmt](b'1234567890')}) as s3:
        assert s3.logical_size('compress/x', fmt) == 10
