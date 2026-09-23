@pytest.mark.parametrize('blocksize', [5, 15, 45, 1500])
def test_read_bytes_delimited(s3, blocksize):
    _, values = read_bytes(test_bucket_name+'/test/accounts*',
                           blocksize=blocksize, delimiter=b'\n', s3=s3)
    _, values2 = read_bytes(test_bucket_name+'/test/accounts*',
                            blocksize=blocksize, delimiter=b'foo', s3=s3)
    assert ([a.key for a in concat(values)] !=
            [b.key for b in concat(values2)])

    results = compute(*concat(values))
    res = [r for r in results if r]
    assert all(r.endswith(b'\n') for r in res)
    ourlines = b''.join(res).split(b'\n')
    testlines = b"".join(files[k] for k in sorted(files)).split(b'\n')
    assert ourlines == testlines

    # delimiter not at the end
    d = b'}'
    _, values = read_bytes(test_bucket_name+'/test/accounts*',
                           blocksize=blocksize, delimiter=d,
                           s3=s3)
    results = compute(*concat(values))
    res = [r for r in results if r]
    # All should end in } except EOF
    assert sum(r.endswith(b'}') for r in res) == len(res) - 2
    ours = b"".join(res)
    test = b"".join(files[v] for v in sorted(files))
    assert ours == test
