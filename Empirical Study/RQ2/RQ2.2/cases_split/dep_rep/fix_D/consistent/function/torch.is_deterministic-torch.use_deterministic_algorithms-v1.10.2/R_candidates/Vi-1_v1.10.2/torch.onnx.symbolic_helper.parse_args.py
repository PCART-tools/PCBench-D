def parse_args(*arg_descriptors):
    """A decorator which converts args from torch._C.Value to built-in types.

    For example:
    @parse_args('v', 'i', 'fs')
    foo(g, a, b, c):
      assert isinstance(a, torch._C.Value)
      assert isinstance(b, int)
      assert isinstance(c, list)
      assert isinstance(c[0], float)

    Args:
      arg_descriptors: list of str, where each element is
        a string that specifies the type to convert to. Valid descriptors:
        "v": no conversion, keep torch._C.Value.
        "i": int
        "is": list(int)
        "f": float
        "fs": list of float
        "b": bool
        "s": str
        "t": torch.Tensor
    """

    def decorator(fn):
        fn._arg_descriptors = arg_descriptors

        @wraps(fn)
        def wrapper(g, *args, **kwargs):
            # some args may be optional, so the length may be smaller
            assert len(arg_descriptors) >= len(args)
            try:
                sig = inspect.signature(fn)
                arg_names = list(sig.parameters.keys())[1:]
                fn_name = fn.__name__
            except Exception:
                arg_names = [None] * len(args)  # type: ignore[list-item]
                fn_name = None
            args = [_parse_arg(arg, arg_desc, arg_name, fn_name)  # type: ignore[assignment]
                    for arg, arg_desc, arg_name in zip(args, arg_descriptors, arg_names)]
            # only support _outputs in kwargs
            assert len(kwargs) <= 1
            if len(kwargs) == 1:
                assert "_outputs" in kwargs
            return fn(g, *args, **kwargs)

        return wrapper
    return decorator
