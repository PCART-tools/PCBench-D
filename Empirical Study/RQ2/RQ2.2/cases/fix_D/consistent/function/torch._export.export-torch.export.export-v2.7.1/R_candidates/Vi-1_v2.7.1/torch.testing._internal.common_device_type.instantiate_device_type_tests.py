def instantiate_device_type_tests(
    generic_test_class,
    scope,
    except_for=None,
    only_for=None,
    include_lazy=False,
    allow_mps=False,
    allow_xpu=False,
):
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
    generic_members = set(generic_test_class.__dict__.keys()) - set(
        empty_class.__dict__.keys()
    )
    generic_tests = [x for x in generic_members if x.startswith("test")]

    # Creates device-specific test cases
    for base in get_desired_device_type_test_bases(
        except_for, only_for, include_lazy, allow_mps, allow_xpu
    ):
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
                    device_type_test_class.instantiate_test(
                        name, copy.deepcopy(test), generic_cls=generic_test_class
                    )
                else:
                    device_type_test_class.instantiate_test(name, copy.deepcopy(test))
            else:  # Ports non-test member
                assert (
                    name not in device_type_test_class.__dict__
                ), f"Redefinition of directly defined member {name}"
                nontest = getattr(generic_test_class, name)
                setattr(device_type_test_class, name, nontest)

        # The dynamically-created test class derives from the test template class
        # and the empty class. Arrange for both setUpClass and tearDownClass methods
        # to be called. This allows the parameterized test classes to support setup
        # and teardown.
        @classmethod
        def _setUpClass(cls):
            base.setUpClass()
            empty_class.setUpClass()

        @classmethod
        def _tearDownClass(cls):
            empty_class.tearDownClass()
            base.tearDownClass()

        device_type_test_class.setUpClass = _setUpClass
        device_type_test_class.tearDownClass = _tearDownClass

        # Mimics defining the instantiated class in the caller's file
        # by setting its module to the given class's and adding
        # the module to the given scope.
        # This lets the instantiated class be discovered by unittest.
        device_type_test_class.__module__ = generic_test_class.__module__
        scope[class_name] = device_type_test_class
