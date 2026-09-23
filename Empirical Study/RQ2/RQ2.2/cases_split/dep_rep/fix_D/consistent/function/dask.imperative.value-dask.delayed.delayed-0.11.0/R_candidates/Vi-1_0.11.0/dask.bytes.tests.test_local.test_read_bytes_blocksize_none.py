def test_read_bytes_blocksize_none():
    with filetexts(files, mode='b'):
        sample, values = read_bytes('.test.accounts.*', blocksize=None)
        assert sum(map(len, values)) == len(files)
