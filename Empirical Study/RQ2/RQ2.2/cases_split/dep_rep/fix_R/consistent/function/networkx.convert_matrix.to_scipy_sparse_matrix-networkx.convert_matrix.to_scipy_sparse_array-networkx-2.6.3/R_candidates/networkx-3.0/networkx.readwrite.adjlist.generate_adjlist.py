def generate_adjlist(G, delimiter=" "):
    """Generate a single line of the graph G in adjacency list format.

    Parameters
    ----------
    G : NetworkX graph

    delimiter : string, optional
       Separator for node labels

    Returns
    -------
    lines : string
        Lines of data in adjlist format.

    Examples
    --------
    >>> G = nx.lollipop_graph(4, 3)
    >>> for line in nx.generate_adjlist(G):
    ...     print(line)
    0 1 2 3
    1 2 3
    2 3
    3 4
    4 5
    5 6
    6

    See Also
    --------
    write_adjlist, read_adjlist

    Notes
    -----
    The default `delimiter=" "` will result in unexpected results if node names contain
    whitespace characters. To avoid this problem, specify an alternate delimiter when spaces are
    valid in node names.

    NB: This option is not available for data that isn't user-generated.

    """
    directed = G.is_directed()
    seen = set()
    for s, nbrs in G.adjacency():
        line = str(s) + delimiter
        for t, data in nbrs.items():
            if not directed and t in seen:
                continue
            if G.is_multigraph():
                for d in data.values():
                    line += str(t) + delimiter
            else:
                line += str(t) + delimiter
        if not directed:
            seen.add(s)
        yield line[: -len(delimiter)]
