@pytest.mark.parametrize(
    ("edge_color", "expected"),
    (
        (None, "black"),  # Default
        ("r", "red"),  # Non-default color string
        (["r"], "red"),  # Single non-default color in a list
        ((1.0, 1.0, 0.0), "yellow"),  # single color as rgb tuple
        ([(1.0, 1.0, 0.0)], "yellow"),  # single color as rgb tuple in list
        ((0, 1, 0, 1), "lime"),  # single color as rgba tuple
        ([(0, 1, 0, 1)], "lime"),  # single color as rgba tuple in list
        ("#0000ff", "blue"),  # single color hex code
        (["#0000ff"], "blue"),  # hex code in list
    ),
)
@pytest.mark.parametrize("edgelist", (None, [(0, 1)]))
def test_single_edge_color_undirected(edge_color, expected, edgelist):
    """Tests ways of specifying all edges have a single color for edges
    drawn with a LineCollection"""

    G = nx.path_graph(3)
    drawn_edges = nx.draw_networkx_edges(
        G, pos=nx.random_layout(G), edgelist=edgelist, edge_color=edge_color
    )
    assert mpl.colors.same_color(drawn_edges.get_color(), expected)
