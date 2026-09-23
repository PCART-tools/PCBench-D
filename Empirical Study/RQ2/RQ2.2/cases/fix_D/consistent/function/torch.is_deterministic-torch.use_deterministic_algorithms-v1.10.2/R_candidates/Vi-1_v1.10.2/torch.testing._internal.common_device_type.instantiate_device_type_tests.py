def instantiate_device_type_tests(generic_test_class, scope, except_for=None, only_for=None):
    # Removes the generic test class from its enclosing scope so its tests
    # are not discoverable.
    del scope[generic_test_class.__name__]

    # Creates an 'empty' version of the generic_test_class
    # Note: we don't inherit from the generic_test_class directly because
    #   that would add its tests to our test classes and they would be
    #   discovered (despite not being runnable). Inherited methods also
    #   can't be removed later, and we can't rely on load_tests because
    #   pytest doesn't support it (as of this writing).
    empty_name = generic_test_class.__name__ + "_base"
    empty_class = type(empty_name, generic_test_class.__bases__, {})

    # Acquires members names
    # See Note [Overriding methods in generic tests]
    generic_members = set(generic_test_class.__dict__.keys()) - set(empty_class.__dict__.keys())
    generic_tests = [x for x in generic_members if x.startswith('test')]

    # Filter out the device types based on user inputs
    desired_device_type_test_bases = filter_desired_device_types(device_type_test_bases,
                                                                 except_for, only_for)

    def split_if_not_empty(x: str):
        return x.split(",") if len(x) != 0 else []

    # Filter out the device types based on environment variables if available
    # Usage:
    # export PYTORCH_TESTING_DEVICE_ONLY_FOR=cuda,cpu
    # export PYTORCH_TESTING_DEVICE_EXCEPT_FOR=xla
    env_only_for = split_if_not_empty(os.getenv(PYTORCH_TESTING_DEVICE_ONLY_FOR_KEY, ''))
    env_except_for = split_if_not_empty(os.getenv(PYTORCH_TESTING_DEVICE_EXCEPT_FOR_KEY, ''))

    desired_device_type_test_bases = filter_desired_device_types(desired_device_type_test_bases,
                                                                 env_except_for, env_only_for)


    # Creates device-specific test cases
    for base in desired_device_type_test_bases:
        # Special-case for ROCm testing -- only test for 'cuda' i.e. ROCm device by default
        # The except_for and only_for cases were already checked above. At this point we only need to check 'cuda'.
        if TEST_WITH_ROCM and base.device_type != 'cuda':
            continue

        class_name = generic_test_class.__name__ + base.device_type.upper()

        # type set to Any and suppressed due to unsupport runtime class:
        # https://github.com/python/mypy/wiki/Unsupported-Python-Features
        device_type_test_class: Any = type(class_name, (base, empty_class), {})

        for name in generic_members:
            if name in generic_tests:  # Instantiates test member
                test = getattr(generic_test_class, name)
                # XLA-compat shim (XLA's instantiate_test takes doesn't take generic_cls)
                sig = inspect.signature(device_type_test_class.instantiate_test)
                if len(sig.parameters) == 3:
                    # Instantiates the device-specific tests
                    device_type_test_class.instantiate_test(name, copy.deepcopy(test), generic_cls=generic_test_class)
                else:
                    device_type_test_class.instantiate_test(name, copy.deepcopy(test))
            else:  # Ports non-test member
                assert name not in device_type_test_class.__dict__, "Redefinition of directly defined member {0}".format(name)
                nontest = getattr(generic_test_class, name)
                setattr(device_type_test_class, name, nontest)

        # Mimics defining the instantiated class in the caller's file
        # by setting its module to the given class's and adding
        # the module to the given scope.
        # This lets the instantiated class be discovered by unittest.
        device_type_test_class.__module__ = generic_test_class.__module__
        scope[class_name] = device_type_test_class
