def test_bad_compression():
    from dask.bytes.core import read_bytes, open_files, open_text_files
    with filetexts(files, mode='b'):
        for func in [read_bytes, open_files, open_text_files]:
            with pytest.raises(ValueError):
                sample, values = func('.test.accounts.*',
                                      compression='not-found')
