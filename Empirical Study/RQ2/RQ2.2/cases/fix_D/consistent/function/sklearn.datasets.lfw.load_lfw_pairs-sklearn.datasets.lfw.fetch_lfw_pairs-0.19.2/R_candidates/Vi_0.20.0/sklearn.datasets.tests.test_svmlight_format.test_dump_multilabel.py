def test_dump_multilabel():
    X = [[1, 0, 3, 0, 5],
         [0, 0, 0, 0, 0],
         [0, 5, 0, 1, 0]]
    y_dense = [[0, 1, 0], [1, 0, 1], [1, 1, 0]]
    y_sparse = sp.csr_matrix(y_dense)
    for y in [y_dense, y_sparse]:
        f = BytesIO()
        dump_svmlight_file(X, y, f, multilabel=True)
        f.seek(0)
        # make sure it dumps multilabel correctly
        assert_equal(f.readline(), b("1 0:1 2:3 4:5\n"))
        assert_equal(f.readline(), b("0,2 \n"))
        assert_equal(f.readline(), b("0,1 1:5 3:1\n"))
