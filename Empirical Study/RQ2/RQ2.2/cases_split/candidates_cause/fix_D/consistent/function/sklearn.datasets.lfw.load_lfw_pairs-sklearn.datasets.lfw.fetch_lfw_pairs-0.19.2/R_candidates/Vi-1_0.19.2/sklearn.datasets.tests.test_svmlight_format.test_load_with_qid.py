def test_load_with_qid():
    # load svmfile with qid attribute
    data = b("""
    3 qid:1 1:0.53 2:0.12
    2 qid:1 1:0.13 2:0.1
    7 qid:2 1:0.87 2:0.12""")
    X, y = load_svmlight_file(BytesIO(data), query_id=False)
    assert_array_equal(y, [3, 2, 7])
    assert_array_equal(X.toarray(), [[.53, .12], [.13, .1], [.87, .12]])
    res1 = load_svmlight_files([BytesIO(data)], query_id=True)
    res2 = load_svmlight_file(BytesIO(data), query_id=True)
    for X, y, qid in (res1, res2):
        assert_array_equal(y, [3, 2, 7])
        assert_array_equal(qid, [1, 1, 2])
        assert_array_equal(X.toarray(), [[.53, .12], [.13, .1], [.87, .12]])
