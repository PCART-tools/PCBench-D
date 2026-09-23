def test_bad_compression():
    with filetexts(files, mode='b'):
        for func in [read_bytes, open_files, open_text_files]:
            with pytest.raises(ValueError):
                sample, values = func('.test.accounts.*',
                                      compression='not-found')
