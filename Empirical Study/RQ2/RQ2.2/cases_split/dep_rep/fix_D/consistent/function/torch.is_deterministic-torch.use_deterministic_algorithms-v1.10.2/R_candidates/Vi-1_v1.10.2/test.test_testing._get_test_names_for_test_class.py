def _get_test_names_for_test_class(test_cls):
    """ Convenience function to get all test names for a given test class. """
    test_names = ['{}.{}'.format(test_cls.__name__, key) for key in test_cls.__dict__
                  if key.startswith('test_')]
    return sorted(test_names)
