@functools.cache
def _discover_entrypoint_backends():
    # importing here so it will pick up the mocked version in test_backends.py
    from importlib.metadata import entry_points

    group_name = "torch_dynamo_backends"
    if sys.version_info < (3, 10):
        eps = entry_points()
        eps = eps[group_name] if group_name in eps else []
        eps = {ep.name: ep for ep in eps}
    else:
        eps = entry_points(group=group_name)
        eps = {name: eps[name] for name in eps.names}
    for backend_name in eps:
        _BACKENDS[backend_name] = eps[backend_name]
