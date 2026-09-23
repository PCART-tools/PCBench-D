def test_registered_open_files():
    with filetexts(files, mode='b'):
        myfiles = open_files('.test.accounts.*')
        assert len(myfiles) == len(files)
        data = []
        for file in myfiles:
            with file as f:
                data.append(f.read())
        assert list(data) == [files[k] for k in sorted(files)]
