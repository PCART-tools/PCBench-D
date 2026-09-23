def test_dtype_complex():
    x = np.arange(24).reshape((4, 6)).astype('f4')
    y = np.arange(24).reshape((4, 6)).astype('i8')
    z = np.arange(24).reshape((4, 6)).astype('i2')

    a = da.from_array(x, chunks=(2, 3))
    b = da.from_array(y, chunks=(2, 3))
    c = da.from_array(z, chunks=(2, 3))

    def assert_eq(a, b):
        return (isinstance(a, np.dtype) and
                isinstance(b, np.dtype) and
                str(a) == str(b))

    assert_eq(a.dtype, x.dtype)
    assert_eq(b.dtype, y.dtype)

    assert_eq((a + 1).dtype, (x + 1).dtype)
    assert_eq((a + b).dtype, (x + y).dtype)
    assert_eq(a.T.dtype, x.T.dtype)
    assert_eq(a[:3].dtype, x[:3].dtype)
    assert_eq((a.dot(b.T)).dtype, (x.dot(y.T)).dtype)

    assert_eq(stack([a, b]).dtype, np.vstack([x, y]).dtype)
    assert_eq(concatenate([a, b]).dtype, np.concatenate([x, y]).dtype)

    assert_eq(b.std().dtype, y.std().dtype)
    assert_eq(c.sum().dtype, z.sum().dtype)
    assert_eq(a.min().dtype, a.min().dtype)
    assert_eq(b.std().dtype, b.std().dtype)
    assert_eq(a.argmin(axis=0).dtype, a.argmin(axis=0).dtype)

    assert_eq(da.sin(c).dtype, np.sin(z).dtype)
    assert_eq(da.exp(b).dtype, np.exp(y).dtype)
    assert_eq(da.floor(a).dtype, np.floor(x).dtype)
    assert_eq(da.isnan(b).dtype, np.isnan(y).dtype)
    with ignoring(ImportError):
        assert da.isnull(b).dtype == 'bool'
        assert da.notnull(b).dtype == 'bool'

    x = np.array([('a', 1)], dtype=[('text', 'S1'), ('numbers', 'i4')])
    d = da.from_array(x, chunks=(1,))

    assert_eq(d['text'].dtype, x['text'].dtype)
    assert_eq(d[['numbers', 'text']].dtype, x[['numbers', 'text']].dtype)
