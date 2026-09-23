def decorate_test_fn(test_fn, test_cuda, has_impl_parity, device):
    if device == 'cuda':
        test_fn = unittest.skipIf(not TEST_CUDA, "CUDA unavailable")(test_fn)
        test_fn = unittest.skipIf(not test_cuda, "Excluded from CUDA tests")(test_fn)

    # If `Implementation Parity` entry in parity table for this module is `No`,
    # or `has_parity` entry in test params dict is `False`, we mark the test as
    # expected failure.
    if not has_impl_parity:
        test_fn = unittest.expectedFailure(test_fn)

    return test_fn
