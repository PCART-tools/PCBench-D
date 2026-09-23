@open_file(0, mode="r")
def read_dot(path):
    """Returns a NetworkX :class:`MultiGraph` or :class:`MultiDiGraph` from the
    dot file with the passed path.

    If this file contains multiple graphs, only the first such graph is
    returned. All graphs _except_ the first are silently ignored.

    Parameters
    ----------
    path : str or file
        Filename or file handle.

    Returns
    -------
    G : MultiGraph or MultiDiGraph
        A :class:`MultiGraph` or :class:`MultiDiGraph`.

    Notes
    -----
    Use `G = nx.Graph(nx.nx_pydot.read_dot(path))` to return a :class:`Graph` instead of a
    :class:`MultiGraph`.
    """
    import pydot

    msg = (
        "nx.nx_pydot.read_dot depends on the pydot package, which has"
        "known issues and is not actively maintained. Consider using"
        "nx.nx_agraph.read_dot instead.\n\n"
        "See https://github.com/networkx/networkx/issues/5723"
    )
    warnings.warn(msg, DeprecationWarning, stacklevel=2)

    data = path.read()

    # List of one or more "pydot.Dot" instances deserialized from this file.
    P_list = pydot.graph_from_dot_data(data)

    # Convert only the first such instance into a NetworkX graph.
    return from_pydot(P_list[0])
