@pytest.mark.parametrize('fmt,blocksize', fmt_bs)
def test_compression(s3, fmt, blocksize):
    with s3_context('compress', valmap(compress[fmt], files)):
        sample, values = read_bytes('s3://compress/test/accounts.*',
                                    compression=fmt, blocksize=blocksize)
        assert sample.startswith(files[sorted(files)[0]][:10])
        assert sample.endswith(b'\n')

        results = compute(*concat(values))
        assert b''.join(results) == b''.join([files[k] for k in sorted(files)])
