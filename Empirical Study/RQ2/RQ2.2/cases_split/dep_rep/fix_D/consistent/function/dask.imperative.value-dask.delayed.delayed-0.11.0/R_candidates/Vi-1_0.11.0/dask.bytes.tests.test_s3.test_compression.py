@pytest.mark.parametrize('fmt,blocksize', fmt_bs)
def test_compression(s3, fmt, blocksize):
    with s3_context('compress', valmap(compress[fmt], files)) as s3:
        sample, values = read_bytes('compress/test/accounts.*', s3=s3,
                                    compression=fmt, blocksize=blocksize)
        assert sample.startswith(files[sorted(files)[0]][:10])

        results = compute(*concat(values))
        assert b''.join(results) == b''.join([files[k] for k in sorted(files)])
