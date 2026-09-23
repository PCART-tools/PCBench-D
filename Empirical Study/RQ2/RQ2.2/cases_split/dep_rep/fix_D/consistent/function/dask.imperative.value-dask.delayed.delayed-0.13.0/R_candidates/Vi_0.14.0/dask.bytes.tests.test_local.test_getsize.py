@pytest.mark.parametrize('fmt', list(compression.seekable_files))
def test_getsize(fmt):
    fs = LocalFileSystem()
    compress = compression.compress[fmt]
    with filetexts({'.tmp.getsize': compress(b'1234567890')}, mode='b'):
        assert fs.logical_size('.tmp.getsize', fmt) == 10
