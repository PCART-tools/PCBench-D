@pytest.fixture(autouse=True)
def set_warnings():
    warnings.filterwarnings(
        "ignore",
        category=DeprecationWarning,
        message="literal_stringizer is deprecated",
    )
    warnings.filterwarnings(
        "ignore",
        category=DeprecationWarning,
        message="literal_destringizer is deprecated",
    )
    # create_using for scale_free_graph
    warnings.filterwarnings(
        "ignore", category=DeprecationWarning, message="The create_using argument"
    )
    warnings.filterwarnings(
        "ignore", category=DeprecationWarning, message="nx.nx_pydot"
    )
    warnings.filterwarnings(
        "ignore",
        category=DeprecationWarning,
        message="\n\nThe `attrs` keyword argument of node_link",
    )
