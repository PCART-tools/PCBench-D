def test_rectangle_selector():
    check_rectangle()

    with pytest.warns(
        MatplotlibDeprecationWarning,
            match="Support for drawtype='line' is deprecated"):
        check_rectangle(drawtype='line', useblit=False)

    check_rectangle(useblit=True, button=1)

    with pytest.warns(
        MatplotlibDeprecationWarning,
            match="Support for drawtype='none' is deprecated"):
        check_rectangle(drawtype='none', minspanx=10, minspany=10)

    check_rectangle(minspanx=10, minspany=10, spancoords='pixels')
    check_rectangle(props=dict(fill=True))
