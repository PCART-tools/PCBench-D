def instantiate_parametrized_tests(generic_cls):
    """
    Instantiates tests that have been decorated with a parametrize_fn. This is generally performed by a
    decorator subclass of _TestParametrizer. The generic test will be replaced on the test class by
    parametrized tests with specialized names.

    Args:
        generic_cls (class): Generic test class object containing tests (e.g. TestFoo)
    """
    for attr_name in tuple(dir(generic_cls)):
        class_attr = getattr(generic_cls, attr_name)
        if not hasattr(class_attr, 'parametrize_fn'):
            continue

        # Remove the generic test from the test class.
        delattr(generic_cls, attr_name)

        # Add parametrized tests to the test class.
        def instantiate_test_helper(cls, name, test, param_kwargs):
            @wraps(test)
            def instantiated_test(self, param_kwargs=param_kwargs):
                test(self, **param_kwargs)

            assert not hasattr(generic_cls, name), "Redefinition of test {0}".format(name)
            setattr(generic_cls, name, instantiated_test)

        for (test, test_suffix, param_kwargs) in class_attr.parametrize_fn(
                class_attr, generic_cls=generic_cls, device_cls=None):
            full_name = '{}_{}'.format(test.__name__, test_suffix)
            instantiate_test_helper(cls=generic_cls, name=full_name, test=test, param_kwargs=param_kwargs)
