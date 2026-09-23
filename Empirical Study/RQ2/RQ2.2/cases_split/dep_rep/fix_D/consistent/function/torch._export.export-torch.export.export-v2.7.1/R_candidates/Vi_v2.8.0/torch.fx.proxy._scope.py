    def _scope(method):
        def impl(*args, **kwargs):
            tracer = args[0].tracer
            target = getattr(operator, method)
            return tracer.create_proxy("call_function", target, args, kwargs)

        impl.__name__ = method
        as_magic = f"__{method.strip('_')}__"
        setattr(Proxy, as_magic, impl)
