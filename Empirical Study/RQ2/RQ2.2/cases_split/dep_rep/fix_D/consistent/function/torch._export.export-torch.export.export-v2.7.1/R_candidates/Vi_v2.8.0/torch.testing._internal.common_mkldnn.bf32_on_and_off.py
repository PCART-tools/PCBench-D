def bf32_on_and_off(bf32_precision=1e-5):
    def with_bf32_disabled(self, function_call):
        with bf32_off():
            function_call()

    def with_bf32_enabled(self, function_call):
        with bf32_on(self, bf32_precision):
            function_call()

    def wrapper(f):
        params = inspect.signature(f).parameters
        arg_names = tuple(params.keys())

        @functools.wraps(f)
        def wrapped(*args, **kwargs):
            kwargs.update(zip(arg_names, args))
            cond = bf32_is_not_fp32()
            if "device" in kwargs:
                cond = cond and (torch.device(kwargs["device"]).type == "cpu")
            if "dtype" in kwargs:
                cond = cond and (kwargs["dtype"] == torch.float)
            if cond:
                with_bf32_disabled(kwargs["self"], lambda: f(**kwargs))
                with_bf32_enabled(kwargs["self"], lambda: f(**kwargs))
            else:
                f(**kwargs)

        return wrapped

    return wrapper
