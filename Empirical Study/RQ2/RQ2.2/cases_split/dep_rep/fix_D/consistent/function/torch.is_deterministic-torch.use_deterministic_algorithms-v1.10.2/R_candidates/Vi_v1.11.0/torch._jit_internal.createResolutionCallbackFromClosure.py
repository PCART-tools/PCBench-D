def createResolutionCallbackFromClosure(fn):
    """
    Create a resolutionCallback by introspecting the function instead of
    looking up the stack for the enclosing scope
    """
    closure = get_closure(fn)

    class closure_lookup(object):
        # This is a class since `closure` is a dict and it's easier in
        # `env_helper` if everything just works with `getattr` calls
        def __getattr__(self, key):
            if key in closure:
                return closure[key]
            elif hasattr(typing, key):
                return getattr(typing, key)
            elif hasattr(builtins, key):
                return getattr(builtins, key)
            return None

    return createResolutionCallbackFromEnv(closure_lookup())
