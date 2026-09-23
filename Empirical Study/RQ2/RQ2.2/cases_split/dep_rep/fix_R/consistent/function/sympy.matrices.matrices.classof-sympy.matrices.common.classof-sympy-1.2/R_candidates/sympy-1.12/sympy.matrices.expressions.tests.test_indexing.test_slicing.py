def test_slicing():
    A.as_explicit()[0, :]  # does not raise an error
