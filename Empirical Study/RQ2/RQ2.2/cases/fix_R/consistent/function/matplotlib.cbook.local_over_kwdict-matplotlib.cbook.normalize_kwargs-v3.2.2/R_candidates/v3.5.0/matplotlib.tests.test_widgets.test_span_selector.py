def test_span_selector():
    check_span('horizontal', minspan=10, useblit=True)
    check_span('vertical', onmove_callback=True, button=1)
    check_span('horizontal', props=dict(fill=True))
    check_span('horizontal', interactive=True)
