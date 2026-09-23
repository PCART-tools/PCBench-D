def test_dump_query_id():
    # test dumping a file with query_id
    X, y = load_svmlight_file(datafile)
    X = X.toarray()
    query_id = np.arange(X.shape[0]) // 2
    f = BytesIO()
    dump_svmlight_file(X, y, f, query_id=query_id, zero_based=True)

    f.seek(0)
    X1, y1, query_id1 = load_svmlight_file(f, query_id=True, zero_based=True)
    assert_array_almost_equal(X, X1.toarray())
    assert_array_almost_equal(y, y1)
    assert_array_almost_equal(query_id, query_id1)
