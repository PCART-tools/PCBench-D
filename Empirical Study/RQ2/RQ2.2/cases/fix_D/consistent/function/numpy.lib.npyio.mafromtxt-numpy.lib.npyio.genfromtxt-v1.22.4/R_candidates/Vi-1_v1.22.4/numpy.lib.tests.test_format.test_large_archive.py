@pytest.mark.skipif(np.dtype(np.intp).itemsize < 8,
                    reason="test requires 64-bit system")
@pytest.mark.slow
def test_large_archive(tmpdir):
    # Regression test for product of saving arrays with dimensions of array
    # having a product that doesn't fit in int32.  See gh-7598 for details.
    try:
        a = np.empty((2**30, 2), dtype=np.uint8)
    except MemoryError:
        pytest.skip("Could not create large file")

    fname = os.path.join(tmpdir, "large_archive")

    with open(fname, "wb") as f:
        np.savez(f, arr=a)

    with open(fname, "rb") as f:
        new_a = np.load(f)["arr"]

    assert_(a.shape == new_a.shape)
