@open_file(0, mode="r")
@nx._dispatchable(graphs=None, returns_graph=True)
def read_p2g(path, encoding="utf-8"):
    """Read graph in p2g format from path.

    Returns
    -------
    MultiDiGraph

    Notes
    -----
    If you want a DiGraph (with no self loops allowed and no edge data)
    use D=nx.DiGraph(read_p2g(path))
    """
    lines = (line.decode(encoding) for line in path)
    G = parse_p2g(lines)
    return G
