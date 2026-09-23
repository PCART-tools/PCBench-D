@pytest.mark.parametrize('fmt', list(compression.seekable_files))
def test_getsize(fmt):
    compress = compression.compress[fmt]
    with filetexts({'.tmp.getsize': compress(b'1234567890')}, mode='b'):
        assert getsize('.tmp.getsize', fmt) == 10
