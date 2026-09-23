@pytest.mark.skipif(
    LooseVersion(np.__version__) < '1.12.0',
    reason=textwrap.dedent(
        """\
            NumPy piecewise mishandles the otherwise condition pre-1.12.0.

            xref: https://github.com/numpy/numpy/issues/5737
        """
    )
)
def test_piecewise_otherwise():
    np.random.seed(1337)

    x = np.random.randint(10, size=(15, 16))
    d = da.from_array(x, chunks=(4, 5))

    assert_eq(
        np.piecewise(
            x,
            [x > 5, x <= 2],
            [lambda e, v, k: e + 1, lambda e, v, k: v * e, lambda e, v, k: 0],
            1, k=2
        ),
        da.piecewise(
            d,
            [d > 5, d <= 2],
            [lambda e, v, k: e + 1, lambda e, v, k: v * e, lambda e, v, k: 0],
            1, k=2
        )
    )
