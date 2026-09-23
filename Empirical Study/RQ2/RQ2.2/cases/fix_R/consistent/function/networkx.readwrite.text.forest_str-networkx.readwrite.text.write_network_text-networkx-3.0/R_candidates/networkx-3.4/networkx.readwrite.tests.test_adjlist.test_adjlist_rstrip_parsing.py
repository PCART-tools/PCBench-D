@pytest.mark.parametrize(
    ("lines", "delim"),
    (
        (["1 2 5", "2 3 4", "3 5", "4", "5"], None),  # No extra whitespace
        (["1\t2\t5", "2\t3\t4", "3\t5", "4", "5"], "\t"),  # tab-delimited
        (
            ["1\t2\t5", "2\t3\t4", "3\t5\t", "4\t", "5"],
            "\t",
        ),  # tab-delimited, extra delims
        (
            ["1\t2\t5", "2\t3\t4", "3\t5\t\t\n", "4\t", "5"],
            "\t",
        ),  # extra delim+newlines
    ),
)
def test_adjlist_rstrip_parsing(lines, delim):
    """Regression test related to gh-7465"""
    expected = nx.Graph([(1, 2), (1, 5), (2, 3), (2, 4), (3, 5)])
    nx.utils.graphs_equal(nx.parse_adjlist(lines, delimiter=delim), expected)
