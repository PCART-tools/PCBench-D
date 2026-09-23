def test_load_with_long_qid():
    # load svmfile with longint qid attribute
    data = b("""
    1 qid:0 0:1 1:2 2:3
    0 qid:72048431380967004 0:1440446648 1:72048431380967004 2:236784985
    0 qid:-9223372036854775807 0:1440446648 1:72048431380967004 2:236784985
    3 qid:9223372036854775807  0:1440446648 1:72048431380967004 2:236784985""")
    X, y, qid = load_svmlight_file(BytesIO(data), query_id=True)

    true_X = [[1,          2,                 3],
             [1440446648, 72048431380967004, 236784985],
             [1440446648, 72048431380967004, 236784985],
             [1440446648, 72048431380967004, 236784985]]

    true_y = [1, 0, 0, 3]
    trueQID = [0, 72048431380967004, -9223372036854775807, 9223372036854775807]
    assert_array_equal(y, true_y)
    assert_array_equal(X.toarray(), true_X)
    assert_array_equal(qid, trueQID)

    f = BytesIO()
    dump_svmlight_file(X, y, f, query_id=qid, zero_based=True)
    f.seek(0)
    X, y, qid = load_svmlight_file(f, query_id=True, zero_based=True)
    assert_array_equal(y, true_y)
    assert_array_equal(X.toarray(), true_X)
    assert_array_equal(qid, trueQID)

    f.seek(0)
    X, y = load_svmlight_file(f, query_id=False, zero_based=True)
    assert_array_equal(y, true_y)
    assert_array_equal(X.toarray(), true_X)
