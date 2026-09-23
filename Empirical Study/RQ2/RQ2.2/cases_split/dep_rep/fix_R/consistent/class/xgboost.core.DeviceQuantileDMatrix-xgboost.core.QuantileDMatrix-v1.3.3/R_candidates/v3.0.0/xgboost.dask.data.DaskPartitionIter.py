class DaskPartitionIter(DataIter):  # pylint: disable=R0902
    """A data iterator for the `DaskQuantileDMatrix`."""

    def __init__(
        self,
        data: List[Any],
        feature_names: Optional[FeatureNames] = None,
        feature_types: Optional[Union[Any, List[Any]]] = None,
        feature_weights: Optional[Any] = None,
        **kwargs: Optional[List[Any]],
    ) -> None:
        types = (Sequence, type(None))
        # Samples
        self._data = data
        for k in meta:
            setattr(self, k, kwargs.get(k, None))
            assert isinstance(getattr(self, k), types)

        # Feature info
        self._feature_names = feature_names
        self._feature_types = feature_types
        self._feature_weights = feature_weights

        assert isinstance(self._data, Sequence)

        self._iter = 0  # set iterator to 0
        super().__init__(release_data=True)

    def _get(self, attr: str) -> Optional[Any]:
        if getattr(self, attr) is not None:
            return getattr(self, attr)[self._iter]
        return None

    def data(self) -> Any:
        """Utility function for obtaining current batch of data."""
        return self._data[self._iter]

    def reset(self) -> None:
        """Reset the iterator"""
        self._iter = 0

    def next(self, input_data: Callable) -> bool:
        """Yield next batch of data"""
        if self._iter == len(self._data):
            # Return False when there's no more batch.
            return False

        kwargs = {k: self._get(k) for k in meta}
        input_data(
            data=self.data(),
            group=None,
            feature_names=self._feature_names,
            feature_types=self._feature_types,
            feature_weights=self._feature_weights,
            **kwargs,
        )
        self._iter += 1
        return True
