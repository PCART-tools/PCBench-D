def test_read_bytes_sample_delimiter():
    with filetexts(files, mode='b'):
        sample, values = read_bytes('.test.accounts.*',
                                    sample=80, delimiter=b'\n')
        assert sample.endswith(b'\n')
        sample, values = read_bytes('.test.accounts.1.json',
                                    sample=80, delimiter=b'\n')
        assert sample.endswith(b'\n')
        sample, values = read_bytes('.test.accounts.1.json',
                                    sample=2, delimiter=b'\n')
        assert sample.endswith(b'\n')
