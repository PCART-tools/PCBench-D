def add_test(unit_test_class, test_name, test_fn):
    if has_test(unit_test_class, test_name):
        raise RuntimeError("Found two tests with the same name: " + test_name)
    setattr(unit_test_class, test_name, test_fn)
