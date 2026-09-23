def match(*signature, **kwargs):
    namespace = kwargs.get('namespace', global_namespace)
    dispatcher = kwargs.get('Dispatcher', Dispatcher)

    def _(func):
        name = func.__name__

        if name not in namespace:
            namespace[name] = dispatcher(name)
        d = namespace[name]

        d.add(signature, func)

        return d
    return _
