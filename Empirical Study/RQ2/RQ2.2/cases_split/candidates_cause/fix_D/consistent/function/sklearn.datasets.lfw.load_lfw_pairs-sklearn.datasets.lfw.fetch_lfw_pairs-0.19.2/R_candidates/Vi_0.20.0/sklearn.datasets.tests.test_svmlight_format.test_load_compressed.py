def test_load_compressed():
    X, y = load_svmlight_file(datafile)

    with NamedTemporaryFile(prefix="sklearn-test", suffix=".gz") as tmp:
        tmp.close()  # necessary under windows
        with open(datafile, "rb") as f:
            with gzip.open(tmp.name, "wb") as fh_out:
                shutil.copyfileobj(f, fh_out)
        Xgz, ygz = load_svmlight_file(tmp.name)
        # because we "close" it manually and write to it,
        # we need to remove it manually.
        os.remove(tmp.name)
    assert_array_almost_equal(X.toarray(), Xgz.toarray())
    assert_array_almost_equal(y, ygz)

    with NamedTemporaryFile(prefix="sklearn-test", suffix=".bz2") as tmp:
        tmp.close()  # necessary under windows
        with open(datafile, "rb") as f:
            with BZ2File(tmp.name, "wb") as fh_out:
                shutil.copyfileobj(f, fh_out)
        Xbz, ybz = load_svmlight_file(tmp.name)
        # because we "close" it manually and write to it,
        # we need to remove it manually.
        os.remove(tmp.name)
    assert_array_almost_equal(X.toarray(), Xbz.toarray())
    assert_array_almost_equal(y, ybz)
