def traverse(datapipe: DataPipe, only_datapipe: Optional[bool] = None) -> DataPipeGraph:
    r"""
    Traverse the DataPipes and their attributes to extract the DataPipe graph.

    [Deprecated]
    When ``only_dataPipe`` is specified as ``True``, it would only look into the
    attribute from each DataPipe that is either a DataPipe and a Python collection object
    such as ``list``, ``tuple``, ``set`` and ``dict``.

    Note:
        This function is deprecated. Please use `traverse_dps` instead.

    Args:
        datapipe: the end DataPipe of the graph
        only_datapipe: If ``False`` (default), all attributes of each DataPipe are traversed.
          This argument is deprecating and will be removed after the next release.
    Returns:
        A graph represented as a nested dictionary, where keys are ids of DataPipe instances
        and values are tuples of DataPipe instance and the sub-graph
    """
    msg = (
        "`traverse` function and will be removed after 1.13. "
        "Please use `traverse_dps` instead."
    )
    if not only_datapipe:
        msg += " And, the behavior will be changed to the equivalent of `only_datapipe=True`."
    warnings.warn(msg, FutureWarning)
    if only_datapipe is None:
        only_datapipe = False
    cache: set[int] = set()
    return _traverse_helper(datapipe, only_datapipe, cache)
