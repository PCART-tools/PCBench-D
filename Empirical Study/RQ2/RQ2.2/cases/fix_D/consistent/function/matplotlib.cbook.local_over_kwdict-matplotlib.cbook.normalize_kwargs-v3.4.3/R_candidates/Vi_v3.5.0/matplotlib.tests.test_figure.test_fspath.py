@pytest.mark.parametrize("fmt", ["png", "pdf", "ps", "eps", "svg"])
def test_fspath(fmt, tmpdir):
    out = Path(tmpdir, "test.{}".format(fmt))
    plt.savefig(out)
    with out.open("rb") as file:
        # All the supported formats include the format name (case-insensitive)
        # in the first 100 bytes.
        assert fmt.encode("ascii") in file.read(100).lower()
