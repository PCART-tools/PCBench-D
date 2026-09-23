def test_dump_comment():
    X, y = load_svmlight_file(datafile)
    X = X.toarray()

    f = BytesIO()
    ascii_comment = "This is a comment\nspanning multiple lines."
    dump_svmlight_file(X, y, f, comment=ascii_comment, zero_based=False)
    f.seek(0)

    X2, y2 = load_svmlight_file(f, zero_based=False)
    assert_array_almost_equal(X, X2.toarray())
    assert_array_equal(y, y2)

    # XXX we have to update this to support Python 3.x
    utf8_comment = b("It is true that\n\xc2\xbd\xc2\xb2 = \xc2\xbc")
    f = BytesIO()
    assert_raises(UnicodeDecodeError,
                  dump_svmlight_file, X, y, f, comment=utf8_comment)

    unicode_comment = utf8_comment.decode("utf-8")
    f = BytesIO()
    dump_svmlight_file(X, y, f, comment=unicode_comment, zero_based=False)
    f.seek(0)

    X2, y2 = load_svmlight_file(f, zero_based=False)
    assert_array_almost_equal(X, X2.toarray())
    assert_array_equal(y, y2)

    f = BytesIO()
    assert_raises(ValueError,
                  dump_svmlight_file, X, y, f, comment="I've got a \0.")
