@open_file(1, mode="w")
def write_dot(G, path):
    """Write NetworkX graph G to Graphviz dot format on path.

    Path can be a string or a file handle.
    """
    msg = (
        "nx.nx_pydot.write_dot depends on the pydot package, which has"
        "known issues and is not actively maintained. Consider using"
        "nx.nx_agraph.write_dot instead.\n\n"
        "See https://github.com/networkx/networkx/issues/5723"
    )
    warnings.warn(msg, DeprecationWarning, stacklevel=2)
    P = to_pydot(G)
    path.write(P.to_string())
    return
