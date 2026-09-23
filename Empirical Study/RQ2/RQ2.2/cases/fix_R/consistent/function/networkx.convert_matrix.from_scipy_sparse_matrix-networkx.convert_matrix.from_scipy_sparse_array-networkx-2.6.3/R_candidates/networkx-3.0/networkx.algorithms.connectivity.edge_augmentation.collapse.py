def collapse(G, grouped_nodes):
    """Collapses each group of nodes into a single node.

    This is similar to condensation, but works on undirected graphs.

    Parameters
    ----------
    G : NetworkX Graph

    grouped_nodes:  list or generator
       Grouping of nodes to collapse. The grouping must be disjoint.
       If grouped_nodes are strongly_connected_components then this is
       equivalent to :func:`condensation`.

    Returns
    -------
    C : NetworkX Graph
       The collapsed graph C of G with respect to the node grouping.  The node
       labels are integers corresponding to the index of the component in the
       list of grouped_nodes.  C has a graph attribute named 'mapping' with a
       dictionary mapping the original nodes to the nodes in C to which they
       belong.  Each node in C also has a node attribute 'members' with the set
       of original nodes in G that form the group that the node in C
       represents.

    Examples
    --------
    >>> # Collapses a graph using disjoint groups, but not necesarilly connected
    >>> G = nx.Graph([(1, 0), (2, 3), (3, 1), (3, 4), (4, 5), (5, 6), (5, 7)])
    >>> G.add_node("A")
    >>> grouped_nodes = [{0, 1, 2, 3}, {5, 6, 7}]
    >>> C = collapse(G, grouped_nodes)
    >>> members = nx.get_node_attributes(C, "members")
    >>> sorted(members.keys())
    [0, 1, 2, 3]
    >>> member_values = set(map(frozenset, members.values()))
    >>> assert {0, 1, 2, 3} in member_values
    >>> assert {4} in member_values
    >>> assert {5, 6, 7} in member_values
    >>> assert {"A"} in member_values
    """
    mapping = {}
    members = {}
    C = G.__class__()
    i = 0  # required if G is empty
    remaining = set(G.nodes())
    for i, group in enumerate(grouped_nodes):
        group = set(group)
        assert remaining.issuperset(
            group
        ), "grouped nodes must exist in G and be disjoint"
        remaining.difference_update(group)
        members[i] = group
        mapping.update((n, i) for n in group)
    # remaining nodes are in their own group
    for i, node in enumerate(remaining, start=i + 1):
        group = {node}
        members[i] = group
        mapping.update((n, i) for n in group)
    number_of_groups = i + 1
    C.add_nodes_from(range(number_of_groups))
    C.add_edges_from(
        (mapping[u], mapping[v]) for u, v in G.edges() if mapping[u] != mapping[v]
    )
    # Add a list of members (ie original nodes) to each node (ie scc) in C.
    nx.set_node_attributes(C, name="members", values=members)
    # Add mapping dict as graph attribute
    C.graph["mapping"] = mapping
    return C
