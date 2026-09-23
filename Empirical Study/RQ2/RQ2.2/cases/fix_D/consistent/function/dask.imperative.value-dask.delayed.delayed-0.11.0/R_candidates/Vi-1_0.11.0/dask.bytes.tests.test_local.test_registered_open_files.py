def test_registered_open_files():
    from dask.bytes.core import open_files
    with filetexts(files, mode='b'):
        myfiles = open_files('.test.accounts.*')
        assert len(myfiles) == len(files)
        data = compute(*[file.read() for file in myfiles])
        assert list(data) == [files[k] for k in sorted(files)]
