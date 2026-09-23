@preserve_random_state
def test_preserve_random_state():
    try:
        import numpy.random

        r = numpy.random.random()
    except ImportError:
        return
    assert abs(r - 0.61879477158568) < 1e-16
