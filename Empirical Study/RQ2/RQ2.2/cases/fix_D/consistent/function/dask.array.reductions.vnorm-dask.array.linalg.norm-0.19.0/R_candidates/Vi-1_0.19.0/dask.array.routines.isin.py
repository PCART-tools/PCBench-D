@safe_wraps(getattr(np, 'isin', None))
def isin(element, test_elements, assume_unique=False, invert=False):
    element = asarray(element)
    test_elements = asarray(test_elements)
    element_axes = tuple(range(element.ndim))
    test_axes = tuple(i + element.ndim for i in range(test_elements.ndim))
    mapped = atop(_isin_kernel, element_axes + test_axes,
                  element, element_axes,
                  test_elements, test_axes,
                  adjust_chunks={axis: lambda _: 1 for axis in test_axes},
                  dtype=bool,
                  assume_unique=assume_unique)
    result = mapped.any(axis=test_axes)
    if invert:
        result = ~result
    return result
