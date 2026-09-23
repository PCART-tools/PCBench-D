def test_load_compressed():
    X, y = load_svmlight_file(datafile)

    with NamedTemporaryFile(prefix="sklearn-test", suffix=".gz") as tmp:
        tmp.close()  # necessary under windows
        with open(datafile, "rb") as f:
            shutil.copyfileobj(f, gzip.open(tmp.name, "wb"))
        Xgz, ygz = load_svmlight_file(tmp.name)
        # because we "close" it manually and write to it,
        # we need to remove it manually.
        os.remove(tmp.name)
    assert_array_equal(X.toarray(), Xgz.toarray())
    assert_array_equal(y, ygz)

    with NamedTemporaryFile(prefix="sklearn-test", suffix=".bz2") as tmp:
        tmp.close()  # necessary under windows
        with open(datafile, "rb") as f:
            shutil.copyfileobj(f, BZ2File(tmp.name, "wb"))
        Xbz, ybz = load_svmlight_file(tmp.name)
        # because we "close" it manually and write to it,
        # we need to remove it manually.
        os.remove(tmp.name)
    assert_array_equal(X.toarray(), Xbz.toarray())
    assert_array_equal(y, ybz)
