def test_dump_concise():
    one = 1
    two = 2.1
    three = 3.01
    exact = 1.000000000000001
    # loses the last decimal place
    almost = 1.0000000000000001
    X = [[one, two, three, exact, almost],
         [1e9, 2e18, 3e27, 0, 0],
         [0, 0, 0, 0, 0],
         [0, 0, 0, 0, 0],
         [0, 0, 0, 0, 0]]
    y = [one, two, three, exact, almost]
    f = BytesIO()
    dump_svmlight_file(X, y, f)
    f.seek(0)
    # make sure it's using the most concise format possible
    assert_equal(f.readline(),
                 b("1 0:1 1:2.1 2:3.01 3:1.000000000000001 4:1\n"))
    assert_equal(f.readline(), b("2.1 0:1000000000 1:2e+18 2:3e+27\n"))
    assert_equal(f.readline(), b("3.01 \n"))
    assert_equal(f.readline(), b("1.000000000000001 \n"))
    assert_equal(f.readline(), b("1 \n"))
    f.seek(0)
    # make sure it's correct too :)
    X2, y2 = load_svmlight_file(f)
    assert_array_almost_equal(X, X2.toarray())
    assert_array_almost_equal(y, y2)
