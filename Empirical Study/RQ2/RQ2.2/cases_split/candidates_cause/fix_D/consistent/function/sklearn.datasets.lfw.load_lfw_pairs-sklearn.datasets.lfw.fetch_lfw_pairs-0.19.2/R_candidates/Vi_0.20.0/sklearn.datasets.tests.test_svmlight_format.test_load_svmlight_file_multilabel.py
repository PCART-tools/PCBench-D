def test_load_svmlight_file_multilabel():
    X, y = load_svmlight_file(multifile, multilabel=True)
    assert_equal(y, [(0, 1), (2,), (), (1, 2)])
