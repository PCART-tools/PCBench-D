@pytest.mark.parametrize('fmt,blocksize', fmt_bs)
def test_compression(fmt, blocksize):
    compress = compression.compress[fmt]
    files2 = valmap(compress, files)
    with filetexts(files2, mode='b'):
        sample, values = read_bytes('.test.accounts.*.json',
                                    blocksize=blocksize, delimiter=b'\n',
                                    compression=fmt)
        assert sample[:5] == files[sorted(files)[0]][:5]
        assert sample.endswith(b'\n')

        results = compute(*concat(values))
        assert (b''.join(results) ==
                b''.join([files[k] for k in sorted(files)]))
