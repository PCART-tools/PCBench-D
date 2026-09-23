def normalize_function(func):
    if isinstance(func, curry):
        func = func._partial
    if isinstance(func, Compose):
        first = getattr(func, 'first', None)
        funcs = reversed((first,) + func.funcs) if first else func.funcs
        return tuple(normalize_function(f) for f in funcs)
    elif isinstance(func, partial):
        kws = tuple(sorted(func.keywords.items())) if func.keywords else ()
        return (normalize_function(func.func), func.args, kws)
    else:
        try:
            result = pickle.dumps(func, protocol=0)
            if b'__main__' not in result:  # abort on dynamic functions
                return result
        except:
            pass
        try:
            import cloudpickle
            return cloudpickle.dumps(func, protocol=0)
        except:
            return str(func)
