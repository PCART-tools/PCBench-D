def from_scipy_sparse_matrix(
    A, parallel_edges=False, create_using=None, edge_attribute="weight"
):
    """Creates a new graph from an adjacency matrix given as a SciPy sparse
    matrix.

    Parameters
    ----------
    A: scipy sparse matrix
      An adjacency matrix representation of a graph

    parallel_edges : Boolean
      If this is True, `create_using` is a multigraph, and `A` is an
      integer matrix, then entry *(i, j)* in the matrix is interpreted as the
      number of parallel edges joining vertices *i* and *j* in the graph.
      If it is False, then the entries in the matrix are interpreted as
      the weight of a single edge joining the vertices.

    create_using : NetworkX graph constructor, optional (default=nx.Graph)
       Graph type to create. If graph instance, then cleared before populated.

    edge_attribute: string
       Name of edge attribute to store matrix numeric value. The data will
       have the same type as the matrix entry (int, float, (real,imag)).

    Notes
    -----
    For directed graphs, explicitly mention create_using=nx.DiGraph,
    and entry i,j of A corresponds to an edge from i to j.

    If `create_using` is :class:`networkx.MultiGraph` or
    :class:`networkx.MultiDiGraph`, `parallel_edges` is True, and the
    entries of `A` are of type :class:`int`, then this function returns a
    multigraph (constructed from `create_using`) with parallel edges.
    In this case, `edge_attribute` will be ignored.

    If `create_using` indicates an undirected multigraph, then only the edges
    indicated by the upper triangle of the matrix `A` will be added to the
    graph.

    Examples
    --------
    >>> import scipy as sp
    >>> import scipy.sparse  # call as sp.sparse
    >>> A = sp.sparse.eye(2, 2, 1)
    >>> G = nx.from_scipy_sparse_matrix(A)

    If `create_using` indicates a multigraph and the matrix has only integer
    entries and `parallel_edges` is False, then the entries will be treated
    as weights for edges joining the nodes (without creating parallel edges):

    >>> A = sp.sparse.csr_matrix([[1, 1], [1, 2]])
    >>> G = nx.from_scipy_sparse_matrix(A, create_using=nx.MultiGraph)
    >>> G[1][1]
    AtlasView({0: {'weight': 2}})

    If `create_using` indicates a multigraph and the matrix has only integer
    entries and `parallel_edges` is True, then the entries will be treated
    as the number of parallel edges joining those two vertices:

    >>> A = sp.sparse.csr_matrix([[1, 1], [1, 2]])
    >>> G = nx.from_scipy_sparse_matrix(
    ...     A, parallel_edges=True, create_using=nx.MultiGraph
    ... )
    >>> G[1][1]
    AtlasView({0: {'weight': 1}, 1: {'weight': 1}})

    """
    warnings.warn(
        (
            "\n\nThe scipy.sparse array containers will be used instead of matrices\n"
            "in Networkx 3.0. Use `from_scipy_sparse_array` instead."
        ),
        DeprecationWarning,
        stacklevel=2,
    )
    return from_scipy_sparse_array(
        A,
        parallel_edges=parallel_edges,
        create_using=create_using,
        edge_attribute=edge_attribute,
    )
