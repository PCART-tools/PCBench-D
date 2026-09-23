class PartIter(DataIter):
    """Iterator for creating Quantile DMatrix from partitions."""

    def __init__(
        self, data: Dict[str, List], device_id: Optional[int], **kwargs: Any
    ) -> None:
        self._iter = 0
        self._device_id = device_id
        self._data = data
        self._kwargs = kwargs

        super().__init__(release_data=True)

    def _fetch(self, data: Optional[Sequence[pd.DataFrame]]) -> Optional[pd.DataFrame]:
        if not data:
            return None

        if self._device_id is not None:
            import cudf
            import cupy as cp

            # We must set the device after import cudf, which will change the device id to 0
            # See https://github.com/rapidsai/cudf/issues/11386
            cp.cuda.runtime.setDevice(self._device_id)  # pylint: disable=I1101
            return cudf.DataFrame(data[self._iter])

        return data[self._iter]

    def next(self, input_data: Callable) -> bool:
        if self._iter == len(self._data[alias.data]):
            return False
        input_data(
            data=self._fetch(self._data[alias.data]),
            label=self._fetch(self._data.get(alias.label, None)),
            weight=self._fetch(self._data.get(alias.weight, None)),
            base_margin=self._fetch(self._data.get(alias.margin, None)),
            qid=self._fetch(self._data.get(alias.qid, None)),
            **self._kwargs,
        )
        self._iter += 1
        return True

    def reset(self) -> None:
        self._iter = 0
