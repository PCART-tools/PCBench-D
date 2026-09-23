@pytest.mark.parametrize(
    "iterator",
    ((i for i in range(3)), iter([1, 2, 3])),  # generator
)
def test_arbitrary_element_raises(iterator):
    """Value error is raised when input is an iterator."""
    with pytest.raises(ValueError, match="from an iterator"):
        arbitrary_element(iterator)
