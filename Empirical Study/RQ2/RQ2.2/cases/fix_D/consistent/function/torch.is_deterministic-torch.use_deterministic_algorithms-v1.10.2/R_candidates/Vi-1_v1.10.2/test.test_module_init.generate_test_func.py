def generate_test_func(test_cls, module_cls, constructor_arg_db,
                       verify_kwargs=True, module_is_lazy=False, check_nonexistent_arg=True):
    # Generate a function for testing the given module.
    @dtypes(*floating_types())
    def run_test(test_cls, device, dtype, module_cls=module_cls):
        # Check if this module creates parameters or registers buffers.
        # The mock magic here passes through to the real Parameter / register_buffer
        # logic and is only used to check for calls.
        args, kwargs = get_example_args(module_cls, constructor_arg_db)

        # Some modules need to pass factory_kwargs so as not to conflict with existing args such as dtype.
        module_needs_factory_kwargs = 'factory_kwargs' in kwargs
        if module_needs_factory_kwargs:
            del kwargs['factory_kwargs']
            extra_kwargs = {
                'factory_kwargs': {
                    'device': device,
                    'dtype': dtype,
                }
            }
        else:
            extra_kwargs = {
                'device': device,
                'dtype': dtype,
            }

        parameter_new = mock_wrapper(torch.nn.Parameter.__new__)
        with patch.object(torch.nn.Parameter, '__new__', parameter_new):
            register_buffer = mock_wrapper(torch.nn.Module.register_buffer)
            with patch.object(torch.nn.Module, 'register_buffer', register_buffer):
                m = module_cls(*args, **kwargs)
                module_creates_params_or_buffers = parameter_new.mock.called or register_buffer.mock.called

        # == Verify factory kwargs are supported. ==
        if verify_kwargs and module_creates_params_or_buffers:
            args, kwargs = get_example_args(module_cls, constructor_arg_db,
                                            extra_kwargs=extra_kwargs)

            if module_is_lazy:
                # Ensure device and dtype are passed to all UninitializedParameters and UninitializedBuffers.
                uninit_param_new = mock_wrapper(torch.nn.UninitializedParameter.__new__)
                with patch.object(torch.nn.UninitializedParameter, '__new__', uninit_param_new):
                    uninit_buffer_new = mock_wrapper(torch.nn.UninitializedBuffer.__new__)
                    with patch.object(torch.nn.UninitializedBuffer, '__new__', uninit_buffer_new):
                        m = module_cls(*args, **kwargs)
                        uninit_param_new.mock.assert_has_calls(
                            [mock.call(device=device, dtype=dtype) for _ in uninit_param_new.mock.mock_calls])
                        uninit_buffer_new.mock.assert_has_calls(
                            [mock.call(device=device, dtype=dtype) for _ in uninit_buffer_new.mock.mock_calls])
            else:
                # Check device placement and dtype for parameters and buffers.
                # Only verify floating point dtypes since that's what the kwarg applies to.
                # Note that dtype verification is also skipped if the module requires factory_kwargs.
                m = module_cls(*args, **kwargs)
                for name, param in m.named_parameters():
                    test_cls.assertEqual(
                        str(param.device), device,
                        f'Parameter {name} is on {param.device.type} instead of the expected device {device}')
                    if param.dtype.is_floating_point and not module_needs_factory_kwargs:
                        test_cls.assertEqual(
                            param.dtype, dtype,
                            f'Parameter {name} is of dtype {param.dtype} instead of the expected dtype {dtype}')
                for name, buffer in m.named_buffers():
                    test_cls.assertEqual(
                        str(buffer.device), device,
                        f'Buffer {name} is on {buffer.device.type} instead of the expected device {device}')
                    if buffer.dtype.is_floating_point and not module_needs_factory_kwargs:
                        test_cls.assertEqual(
                            buffer.dtype, dtype,
                            f'Buffer {name} is of dtype {buffer.dtype} instead of the expected dtype {dtype}')

        # == Verify passing a nonexistent arg errors out. ==
        if check_nonexistent_arg:
            with test_cls.assertRaises(TypeError):
                m = module_cls(*args, **kwargs, nonexistent_arg='foo')

    return run_test
