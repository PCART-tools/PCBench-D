@pytest.mark.parametrize(
    ("generic_data", "long_datum", "unitless_dtype", "expected_dtype"),
    [
        ("2012-03", "2013-01-15", "M8", "M8[D]"),  # Datetimes
        ("spam-a-lot", "tis_but_a_scratch", "U", "U17"),  # str
    ],
)
@pytest.mark.parametrize("nrows", (10, 50000, 60000))  # lt, eq, gt chunksize
def test_parametric_unit_discovery(
    generic_data, long_datum, unitless_dtype, expected_dtype, nrows
):
    """Check that the correct unit (e.g. month, day, second) is discovered from
    the data when a user specifies a unitless datetime."""
    # Unit should be "D" (days) due to last entry
    data = [generic_data] * 50000 + [long_datum]
    expected = np.array(data, dtype=expected_dtype)

    # file-like path
    txt = StringIO("\n".join(data))
    a = np.loadtxt(txt, dtype=unitless_dtype)
    assert a.dtype == expected.dtype
    assert_equal(a, expected)

    # file-obj path
    fd, fname = mkstemp()
    os.close(fd)
    with open(fname, "w") as fh:
        fh.write("\n".join(data))
    a = np.loadtxt(fname, dtype=unitless_dtype)
    os.remove(fname)
    assert a.dtype == expected.dtype
    assert_equal(a, expected)
