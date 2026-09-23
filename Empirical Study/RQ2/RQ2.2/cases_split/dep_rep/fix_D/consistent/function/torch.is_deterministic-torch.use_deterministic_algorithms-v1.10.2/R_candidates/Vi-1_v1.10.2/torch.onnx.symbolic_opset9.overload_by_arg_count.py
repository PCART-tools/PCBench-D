def overload_by_arg_count(fn):
    @wraps(fn)
    def wrapper(g, *args):
        overloads = fn(g, *args)
        last_exception = None
        for overload in overloads:
            arg_descriptors = overload._arg_descriptors
            if len(arg_descriptors) == len(args):
                return overload(g, *args)
        raise NotImplementedError("Unknown aten::{} signature".format(fn.__name__))
    return wrapper
