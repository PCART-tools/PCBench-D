def _mark_tests(items):
    """Allow backend to mark tests (skip or xfail) if they aren't able to correctly handle them"""
    if os.environ.get("NETWORKX_GRAPH_CONVERT"):
        plugin_name = os.environ["NETWORKX_GRAPH_CONVERT"]
        backend = plugins[plugin_name].load()
        if hasattr(backend, "on_start_tests"):
            getattr(backend, "on_start_tests")(items)
