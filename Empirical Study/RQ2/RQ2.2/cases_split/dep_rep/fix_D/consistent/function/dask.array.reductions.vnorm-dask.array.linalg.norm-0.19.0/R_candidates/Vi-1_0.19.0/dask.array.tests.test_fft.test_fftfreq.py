@pytest.mark.parametrize("n", [1, 2, 3, 6, 7])
@pytest.mark.parametrize("d", [1.0, 0.5, 2 * np.pi])
@pytest.mark.parametrize("c", [lambda m: m, lambda m: (1, m - 1)])
def test_fftfreq(n, d, c):
    c = c(n)

    r1 = np.fft.fftfreq(n, d)
    r2 = da.fft.fftfreq(n, d, chunks=c)

    assert normalize_chunks(c, r2.shape) == r2.chunks

    assert_eq(r1, r2)
