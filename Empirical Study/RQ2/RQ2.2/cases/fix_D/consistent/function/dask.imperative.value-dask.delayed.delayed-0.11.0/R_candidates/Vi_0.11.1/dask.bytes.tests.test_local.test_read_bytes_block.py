def test_read_bytes_block():
    with filetexts(files, mode='b'):
        for bs in [5, 15, 45, 1500]:
            sample, vals = read_bytes('.test.account*', blocksize=bs)
            assert (list(map(len, vals)) ==
                    [(len(v) // bs + 1) for v in files.values()])

            results = compute(*concat(vals))
            assert (sum(len(r) for r in results) ==
                    sum(len(v) for v in files.values()))

            ourlines = b"".join(results).split(b'\n')
            testlines = b"".join(files.values()).split(b'\n')
            assert set(ourlines) == set(testlines)
