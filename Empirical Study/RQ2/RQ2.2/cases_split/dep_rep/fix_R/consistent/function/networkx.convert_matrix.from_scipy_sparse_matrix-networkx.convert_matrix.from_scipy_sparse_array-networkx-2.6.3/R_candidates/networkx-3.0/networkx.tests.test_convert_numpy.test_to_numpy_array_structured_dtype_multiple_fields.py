@pytest.mark.parametrize("graph_type", (nx.Graph, nx.DiGraph))
@pytest.mark.parametrize(
    "edge",
    [
        (0, 1),  # No edge attributes
        (0, 1, {"weight": 10}),  # One edge attr
        (0, 1, {"weight": 5, "flow": -4}),  # Multiple but not all edge attrs
        (0, 1, {"weight": 2.0, "cost": 10, "flow": -45}),  # All attrs
    ],
)
def test_to_numpy_array_structured_dtype_multiple_fields(graph_type, edge):
    G = graph_type([edge])
    dtype = np.dtype([("weight", float), ("cost", float), ("flow", float)])
    A = nx.to_numpy_array(G, dtype=dtype, weight=None)
    for attr in dtype.names:
        expected = nx.to_numpy_array(G, dtype=float, weight=attr)
        npt.assert_array_equal(A[attr], expected)
