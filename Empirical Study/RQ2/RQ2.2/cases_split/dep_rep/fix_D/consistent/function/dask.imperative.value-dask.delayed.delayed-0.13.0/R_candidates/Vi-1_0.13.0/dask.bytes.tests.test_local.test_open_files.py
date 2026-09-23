def test_open_files():
    with filetexts(files, mode='b'):
        myfiles = open_files('.test.accounts.*')
        assert len(myfiles) == len(files)
        for lazy_file, data_file in zip(myfiles, sorted(files)):
            with lazy_file as f:
                x = f.read()
                assert x == files[data_file]
