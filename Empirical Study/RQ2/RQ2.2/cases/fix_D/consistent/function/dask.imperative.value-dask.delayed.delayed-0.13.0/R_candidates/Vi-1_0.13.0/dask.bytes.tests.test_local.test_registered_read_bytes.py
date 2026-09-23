def test_registered_read_bytes():
    from dask.bytes.core import read_bytes
    with filetexts(files, mode='b'):
        sample, values = read_bytes('.test.accounts.*')

        results = compute(*concat(values))
        assert set(results) == set(files.values())
