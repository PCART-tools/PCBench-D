def compare_results(res, desired):
    """Compare lists of arrays."""
    if len(res) != len(desired):
        raise ValueError("Iterables have different lengths")
    # See also PEP 618 for Python 3.10
    for x, y in zip(res, desired):
        assert_array_equal(x, y)
