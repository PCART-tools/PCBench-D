def test_dump():
    X_sparse, y_dense = load_svmlight_file(datafile)
    X_dense = X_sparse.toarray()
    y_sparse = sp.csr_matrix(y_dense)

    # slicing a csr_matrix can unsort its .indices, so test that we sort
    # those correctly
    X_sliced = X_sparse[np.arange(X_sparse.shape[0])]
    y_sliced = y_sparse[np.arange(y_sparse.shape[0])]

    for X in (X_sparse, X_dense, X_sliced):
        for y in (y_sparse, y_dense, y_sliced):
            for zero_based in (True, False):
                for dtype in [np.float32, np.float64, np.int32]:
                    f = BytesIO()
                    # we need to pass a comment to get the version info in;
                    # LibSVM doesn't grok comments so they're not put in by
                    # default anymore.

                    if (sp.issparse(y) and y.shape[0] == 1):
                        # make sure y's shape is: (n_samples, n_labels)
                        # when it is sparse
                        y = y.T

                    dump_svmlight_file(X.astype(dtype), y, f, comment="test",
                                       zero_based=zero_based)
                    f.seek(0)

                    comment = f.readline()
                    try:
                        comment = str(comment, "utf-8")
                    except TypeError:  # fails in Python 2.x
                        pass

                    assert_in("scikit-learn %s" % sklearn.__version__, comment)

                    comment = f.readline()
                    try:
                        comment = str(comment, "utf-8")
                    except TypeError:  # fails in Python 2.x
                        pass

                    assert_in(["one", "zero"][zero_based] + "-based", comment)

                    X2, y2 = load_svmlight_file(f, dtype=dtype,
                                                zero_based=zero_based)
                    assert_equal(X2.dtype, dtype)
                    assert_array_equal(X2.sorted_indices().indices, X2.indices)

                    X2_dense = X2.toarray()

                    if dtype == np.float32:
                        # allow a rounding error at the last decimal place
                        assert_array_almost_equal(
                            X_dense.astype(dtype), X2_dense, 4)
                        assert_array_almost_equal(
                            y_dense.astype(dtype), y2, 4)
                    else:
                        # allow a rounding error at the last decimal place
                        assert_array_almost_equal(
                            X_dense.astype(dtype), X2_dense, 15)
                        assert_array_almost_equal(
                            y_dense.astype(dtype), y2, 15)
