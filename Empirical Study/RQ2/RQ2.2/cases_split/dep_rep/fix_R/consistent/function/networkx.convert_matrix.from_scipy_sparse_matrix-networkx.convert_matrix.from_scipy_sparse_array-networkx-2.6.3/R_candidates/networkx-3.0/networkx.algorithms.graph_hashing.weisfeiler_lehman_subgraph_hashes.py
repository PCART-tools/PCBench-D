def weisfeiler_lehman_subgraph_hashes(
    G, edge_attr=None, node_attr=None, iterations=3, digest_size=16
):
    """
    Return a dictionary of subgraph hashes by node.

    The dictionary is keyed by node to a list of hashes in increasingly
    sized induced subgraphs containing the nodes within 2*k edges
    of the key node for increasing integer k until all nodes are included.

    The function iteratively aggregates and hashes neighbourhoods of each node.
    This is achieved for each step by replacing for each node its label from
    the previous iteration with its hashed 1-hop neighborhood aggregate.
    The new node label is then appended to a list of node labels for each
    node.

    To aggregate neighborhoods at each step for a node $n$, all labels of
    nodes adjacent to $n$ are concatenated. If the `edge_attr` parameter is set,
    labels for each neighboring node are prefixed with the value of this attribute
    along the connecting edge from this neighbor to node $n$. The resulting string
    is then hashed to compress this information into a fixed digest size.

    Thus, at the $i$th iteration nodes within $2i$ distance influence any given
    hashed node label. We can therefore say that at depth $i$ for node $n$
    we have a hash for a subgraph induced by the $2i$-hop neighborhood of $n$.

    Can be used to to create general Weisfeiler-Lehman graph kernels, or
    generate features for graphs or nodes, for example to generate 'words' in a
    graph as seen in the 'graph2vec' algorithm.
    See [1]_ & [2]_ respectively for details.

    Hashes are identical for isomorphic subgraphs and there exist strong
    guarantees that non-isomorphic graphs will get different hashes.
    See [1]_ for details.

    If no node or edge attributes are provided, the degree of each node
    is used as its initial label.
    Otherwise, node and/or edge labels are used to compute the hash.

    Parameters
    ----------
    G: graph
        The graph to be hashed.
        Can have node and/or edge attributes. Can also have no attributes.
    edge_attr: string, default=None
        The key in edge attribute dictionary to be used for hashing.
        If None, edge labels are ignored.
    node_attr: string, default=None
        The key in node attribute dictionary to be used for hashing.
        If None, and no edge_attr given, use the degrees of the nodes as labels.
    iterations: int, default=3
        Number of neighbor aggregations to perform.
        Should be larger for larger graphs.
    digest_size: int, default=16
        Size (in bits) of blake2b hash digest to use for hashing node labels.
        The default size is 16 bits

    Returns
    -------
    node_subgraph_hashes : dict
        A dictionary with each key given by a node in G, and each value given
        by the subgraph hashes in order of depth from the key node.

    Examples
    --------
    Finding similar nodes in different graphs:

    >>> G1 = nx.Graph()
    >>> G1.add_edges_from([
    ...     (1, 2), (2, 3), (2, 4), (3, 5), (4, 6), (5, 7), (6, 7)
    ... ])
    >>> G2 = nx.Graph()
    >>> G2.add_edges_from([
    ...     (1, 3), (2, 3), (1, 6), (1, 5), (4, 6)
    ... ])
    >>> g1_hashes = nx.weisfeiler_lehman_subgraph_hashes(G1, iterations=3, digest_size=8)
    >>> g2_hashes = nx.weisfeiler_lehman_subgraph_hashes(G2, iterations=3, digest_size=8)

    Even though G1 and G2 are not isomorphic (they have different numbers of edges),
    the hash sequence of depth 3 for node 1 in G1 and node 5 in G2 are similar:

    >>> g1_hashes[1]
    ['a93b64973cfc8897', 'db1b43ae35a1878f', '57872a7d2059c1c0']
    >>> g2_hashes[5]
    ['a93b64973cfc8897', 'db1b43ae35a1878f', '1716d2a4012fa4bc']

    The first 2 WL subgraph hashes match. From this we can conclude that it's very
    likely the neighborhood of 4 hops around these nodes are isomorphic: each
    iteration aggregates 1-hop neighbourhoods meaning hashes at depth $n$ are influenced
    by every node within $2n$ hops.

    However the neighborhood of 6 hops is no longer isomorphic since their 3rd hash does
    not match.

    These nodes may be candidates to be classified together since their local topology
    is similar.

    Notes
    -----
    To hash the full graph when subgraph hashes are not needed, use
    `weisfeiler_lehman_graph_hash` for efficiency.

    Similarity between hashes does not imply similarity between graphs.

    References
    ----------
    .. [1] Shervashidze, Nino, Pascal Schweitzer, Erik Jan Van Leeuwen,
       Kurt Mehlhorn, and Karsten M. Borgwardt. Weisfeiler Lehman
       Graph Kernels. Journal of Machine Learning Research. 2011.
       http://www.jmlr.org/papers/volume12/shervashidze11a/shervashidze11a.pdf
    .. [2] Annamalai Narayanan, Mahinthan Chandramohan, Rajasekar Venkatesan,
       Lihui Chen, Yang Liu and Shantanu Jaiswa. graph2vec: Learning
       Distributed Representations of Graphs. arXiv. 2017
       https://arxiv.org/pdf/1707.05005.pdf

    See also
    --------
    weisfeiler_lehman_graph_hash
    """

    def weisfeiler_lehman_step(G, labels, node_subgraph_hashes, edge_attr=None):
        """
        Apply neighborhood aggregation to each node
        in the graph.
        Computes a dictionary with labels for each node.
        Appends the new hashed label to the dictionary of subgraph hashes
        originating from and indexed by each node in G
        """
        new_labels = {}
        for node in G.nodes():
            label = _neighborhood_aggregate(G, node, labels, edge_attr=edge_attr)
            hashed_label = _hash_label(label, digest_size)
            new_labels[node] = hashed_label
            node_subgraph_hashes[node].append(hashed_label)
        return new_labels

    node_labels = _init_node_labels(G, edge_attr, node_attr)

    node_subgraph_hashes = defaultdict(list)
    for _ in range(iterations):
        node_labels = weisfeiler_lehman_step(
            G, node_labels, node_subgraph_hashes, edge_attr
        )

    return dict(node_subgraph_hashes)
