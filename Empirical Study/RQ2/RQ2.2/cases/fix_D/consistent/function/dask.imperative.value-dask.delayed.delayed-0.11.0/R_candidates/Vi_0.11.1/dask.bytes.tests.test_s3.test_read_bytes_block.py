@pytest.mark.parametrize('blocksize', [5, 15, 45, 1500])
def test_read_bytes_block(s3, blocksize):
    _, vals = read_bytes(test_bucket_name + '/test/account*',
                         blocksize=blocksize, s3=s3)
    assert (list(map(len, vals)) ==
            [(len(v) // blocksize + 1) for v in files.values()])

    results = compute(*concat(vals))
    assert (sum(len(r) for r in results) ==
            sum(len(v) for v in files.values()))

    ourlines = b"".join(results).split(b'\n')
    testlines = b"".join(files.values()).split(b'\n')
    assert set(ourlines) == set(testlines)
