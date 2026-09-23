@pytest.mark.parametrize('fmt', list(compression.files))
def test_compression_binary(fmt):
    from dask.bytes.core import open_files
    files2 = valmap(compression.compress[fmt], files)
    with filetexts(files2, mode='b'):
        myfiles = open_files('.test.accounts.*', compression=fmt)
        data = compute(*[file.read() for file in myfiles])
        assert list(data) == [files[k] for k in sorted(files)]
