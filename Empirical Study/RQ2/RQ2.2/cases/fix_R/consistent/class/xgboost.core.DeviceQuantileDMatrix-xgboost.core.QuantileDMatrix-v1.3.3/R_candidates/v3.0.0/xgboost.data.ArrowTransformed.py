class ArrowTransformed(TransformedDf):
    """A storage class for transformed arrow table."""

    def __init__(
        self, columns: List[Union["pa.NumericArray", "pa.DictionaryArray"]]
    ) -> None:
        self.columns = columns

    def array_interface(self) -> bytes:
        """Return a byte string for JSON encoded array interface."""
        if TYPE_CHECKING:
            import pyarrow as pa
        else:
            pa = import_pyarrow()

        def array_inf(col: Union["pa.NumericArray", "pa.DictionaryArray"]) -> ArrayInf:
            buffers = col.buffers()
            if isinstance(col, pa.DictionaryArray):
                mask, _, data = col.buffers()
            else:
                mask, data = buffers

            assert data.is_cpu
            assert col.offset == 0

            jdata = make_array_interface(
                data.address,
                shape=(len(col),),
                dtype=_arrow_npdtype()[col.type],
                is_cuda=not data.is_cpu,
            )
            if mask is not None:
                jmask: ArrayInf = {
                    "data": (mask.address, True),
                    "typestr": "<t1",
                    "version": 3,
                    "strides": None,
                    "shape": (len(col),),
                    "mask": None,
                }
                if not data.is_cpu:
                    jmask["stream"] = 2  # type: ignore
                jdata["mask"] = jmask
            return jdata

        arrays = list(map(array_inf, self.columns))
        sarrays = bytes(json.dumps(arrays), "utf-8")
        return sarrays

    @property
    def shape(self) -> Tuple[int, int]:
        """Return shape of the transformed DataFrame."""
        return len(self.columns[0]), len(self.columns)
