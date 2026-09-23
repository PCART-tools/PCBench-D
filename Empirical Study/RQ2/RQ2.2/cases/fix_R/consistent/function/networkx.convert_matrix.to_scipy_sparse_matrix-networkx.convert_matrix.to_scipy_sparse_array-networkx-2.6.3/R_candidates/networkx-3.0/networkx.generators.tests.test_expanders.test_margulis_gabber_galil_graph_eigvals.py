@pytest.mark.parametrize("n", (2, 3, 5, 6, 10))
def test_margulis_gabber_galil_graph_eigvals(n):
    np = pytest.importorskip("numpy")
    sp = pytest.importorskip("scipy")
    import scipy.linalg

    g = nx.margulis_gabber_galil_graph(n)
    # Eigenvalues are already sorted using the scipy eigvalsh,
    # but the implementation in numpy does not guarantee order.
    w = sorted(sp.linalg.eigvalsh(nx.adjacency_matrix(g).toarray()))
    assert w[-2] < 5 * np.sqrt(2)
