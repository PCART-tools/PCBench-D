def GetGraphPngSafe(func, *args, **kwargs):
    """
    Invokes `func` (e.g. GetPydotGraph) with args. If anything fails - returns
    and empty image instead of throwing Exception
    """
    try:
        graph = func(*args, **kwargs)
        if not isinstance(graph, pydot.Dot):
            raise ValueError("func is expected to return pydot.Dot")
        return graph.create_png()
    except Exception as e:
        logger.error("Failed to draw graph: {}".format(e))
        return _DummyPngImage
