def _isin_kernel(element, test_elements, assume_unique=False):
    values = np.in1d(element.ravel(), test_elements,
                     assume_unique=assume_unique)
    return values.reshape(element.shape + (1,) * test_elements.ndim)
