@pytest.mark.parametrize('fmt,bs,encoding', fmt_bs_enc)
def test_read_text(fmt, bs, encoding):
    compress = compression.compress[fmt]
    files2 = dict((k, compress(v.encode(encoding))) for k, v in files.items())
    with filetexts(files2, mode='b'):
        b = read_text('.test.accounts.*.json', compression=fmt, blocksize=bs,
                      encoding=encoding)
        L, = compute(b)
        assert ''.join(L) == expected

        blocks = read_text('.test.accounts.*.json', compression=fmt, blocksize=bs,
                           encoding=encoding, collection=False)
        L = compute(*blocks)
        assert ''.join(line for block in L for line in block) == expected
