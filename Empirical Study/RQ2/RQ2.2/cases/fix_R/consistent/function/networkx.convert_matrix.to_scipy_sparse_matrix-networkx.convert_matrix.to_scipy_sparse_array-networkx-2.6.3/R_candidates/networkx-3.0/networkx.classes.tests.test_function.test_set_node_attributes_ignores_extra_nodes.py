@pytest.mark.parametrize(
    ("values", "name"),
    (
        ({0: "red", 1: "blue"}, "color"),  # values dictionary
        ({0: {"color": "red"}, 1: {"color": "blue"}}, None),  # dict-of-dict
    ),
)
def test_set_node_attributes_ignores_extra_nodes(values, name):
    """
    When `values` is a dict or dict-of-dict keyed by nodes, ensure that keys
    that correspond to nodes not in G are ignored.
    """
    G = nx.Graph()
    G.add_node(0)
    nx.set_node_attributes(G, values, name)
    assert G.nodes[0]["color"] == "red"
    assert 1 not in G.nodes
