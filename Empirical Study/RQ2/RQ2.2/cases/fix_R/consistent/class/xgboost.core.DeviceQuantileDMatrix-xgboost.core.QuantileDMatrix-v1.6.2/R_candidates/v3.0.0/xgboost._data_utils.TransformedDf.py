class TransformedDf(Protocol):
    """Protocol class for storing transformed dataframe."""

    def array_interface(self) -> bytes:
        """Get a JSON-encoded list of array interfaces."""

    @property
    def shape(self) -> Tuple[int, int]:
        """Return the shape of the dataframe."""
