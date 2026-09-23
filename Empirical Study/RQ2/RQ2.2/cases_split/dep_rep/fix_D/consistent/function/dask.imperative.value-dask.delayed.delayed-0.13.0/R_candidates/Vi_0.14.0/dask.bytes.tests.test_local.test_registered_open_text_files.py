@pytest.mark.parametrize('encoding', ['utf-8', 'ascii'])
def test_registered_open_text_files(encoding):
    from dask.bytes.core import open_text_files
    with filetexts(files, mode='b'):
        myfiles = open_text_files('.test.accounts.*', encoding=encoding)
        assert len(myfiles) == len(files)
        data = []
        for file in myfiles:
            with file as f:
                data.append(f.read())
        assert list(data) == [files[k].decode(encoding)
                              for k in sorted(files)]
