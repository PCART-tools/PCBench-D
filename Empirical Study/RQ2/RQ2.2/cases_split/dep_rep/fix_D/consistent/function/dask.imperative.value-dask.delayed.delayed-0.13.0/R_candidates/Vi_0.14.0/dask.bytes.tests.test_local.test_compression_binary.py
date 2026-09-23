@pytest.mark.parametrize('fmt', list(compression.files))
def test_compression_binary(fmt):
    files2 = valmap(compression.compress[fmt], files)
    with filetexts(files2, mode='b'):
        myfiles = open_files('.test.accounts.*', compression=fmt)
        data = []
        for file in myfiles:
            with file as f:
                data.append(f.read())
        assert list(data) == [files[k] for k in sorted(files)]
