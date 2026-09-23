class PandasTransformed(TransformedDf):
    """A storage class for transformed pandas DataFrame."""

    def __init__(self, columns: List[np.ndarray]) -> None:
        self.columns = columns

    def array_interface(self) -> bytes:
        """Return a byte string for JSON encoded array interface."""
        aitfs = list(map(array_interface_dict, self.columns))
        sarrays = bytes(json.dumps(aitfs), "utf-8")
        return sarrays

    @property
    def shape(self) -> Tuple[int, int]:
        """Return shape of the transformed DataFrame."""
        return self.columns[0].shape[0], len(self.columns)
