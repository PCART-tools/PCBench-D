def generate_tensor_like_override_tests(cls):
    from torch.testing._internal.generated.annotated_fn_args import annotated_args

    def test_generator(func, override):
        # If func corresponds to a torch.Tensor method or property.
        if is_tensor_method_or_property(func):
            # Generate an instance by using SubTensor,
            def instance_gen():
                return SubTensor([5])
        else:
            # Otherwise, TensorLike.
            def instance_gen():
                return TensorLike()

        func_args = []
        is_method = is_tensor_method_or_property(func)
        if func in annotated_args:
            for arg in annotated_args[func]:
                # Guess valid input to aten function based on type of argument
                t = arg['simple_type']
                if t.endswith('?'):
                    t = t[:-1]
                if t == 'Tensor':
                    if is_method and arg['name'] == 'self':
                        # See "Note: properties and __get__"
                        func = func.__get__(instance_gen())
                        continue
                    func_args.append(instance_gen())
                elif t == 'TensorList':
                    func_args.append([instance_gen(), instance_gen()])
                elif t == 'c10::List<c10::optional<Tensor>>':
                    func_args.append([instance_gen(), instance_gen()])
                elif t == 'IntArrayRef':
                    size = arg.get('size', 2)
                    if size == 1:
                        func_args.append(1)
                    else:
                        func_args.append([1] * size)
                elif t == 'Scalar':
                    func_args.append(3.5)
                elif t == 'bool':
                    func_args.append(False)
                elif t.startswith('int') or t in {'Dimname', 'DimnameList'}:
                    func_args.append(0)
                elif t in {'Stream'}:
                    func_args.append(torch.Stream())
                elif t.startswith('float') or t == 'double':
                    func_args.append(1.0)
                elif t in {'Generator', 'MemoryFormat', 'TensorOptions'}:
                    func_args.append(None)
                elif t == 'ScalarType':
                    func_args.append(torch.float32)
                elif t == 'c10::string_view':
                    func_args.append('')
                else:
                    raise RuntimeError(f"Unsupported argument type {t} for {arg['name']} of function {func}")
        else:
            args = inspect.getfullargspec(override)
            try:
                func_args = inspect.getfullargspec(func)
                # Remove annotations from argspec
                func_args = type(func_args)(**{**func_args, 'annotations': None})
                if func_args != args:
                    raise RuntimeError(f"Override for {func} doesn't match its argspec.\n"
                                       + f"Original: {inspect.signature(func)}\n"
                                       + f"Override: {inspect.signature(override)}")
            except TypeError:
                pass
            nargs = len(args.args)
            if args.defaults is not None:
                nargs -= len(args.defaults)
            func_args = [instance_gen() for _ in range(nargs)]
            if args.varargs is not None:
                func_args += [instance_gen(), instance_gen()]

        def test(self):
            ret = func(*func_args)
            # ret is None for certain protocols, e.g., `__weakref__` and `__setitem__`
            # This is currently the best check but doesn't work for, for example,
            # Tensor.__add__ because it redirects to Tensor.add.
            # See note "_triggered wrapper"
            if not is_method or ret is None:
                self.assertTrue(WRAPPED_TRIGGERED_IMPLS[func]._triggered)
                return

            self.assertEqual(ret, -1)

        return test

    for func, override in get_testing_overrides().items():
        test_method = test_generator(func, override)
        if func.__name__ == "__get__":
            # Note: properties and __get__
            # __get__ is part of the descriptor protocol.
            # https://docs.python.org/3/howto/descriptor.html
            # This is used for properties of the form
            # torch.Tensor.<property>, with the method __get__
            # In this case we get the property name in two ways:

            # This case for properties defined in C.
            module = getattr(
                func.__self__,
                "__qualname__",
                None
            )

            # This one for properties defined in Python.
            if module is None:
                module = "Tensor." + func.__self__.fget.__name__

            # Unfortunately I couldn't find a way to unify these two cases
            # and there is no way for general descriptors.
        elif is_tensor_method_or_property(func):
            module = "Tensor"
        else:
            module = func.__module__
        if module:
            name = 'test_{}_{}'.format(module.replace('.', '_'), func.__name__)
        else:
            name = 'test_{}'.format(func.__name__)
        test_method.__name__ = name
        setattr(cls, name, test_method)
