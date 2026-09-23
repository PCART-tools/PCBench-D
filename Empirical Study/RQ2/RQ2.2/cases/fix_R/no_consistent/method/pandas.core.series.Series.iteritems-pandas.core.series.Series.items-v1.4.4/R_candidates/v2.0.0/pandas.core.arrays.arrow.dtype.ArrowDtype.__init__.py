    def __init__(self, pyarrow_dtype: pa.DataType) -> None:
        super().__init__("pyarrow")
        if pa_version_under7p0:
            raise ImportError("pyarrow>=7.0.0 is required for ArrowDtype")
        if not isinstance(pyarrow_dtype, pa.DataType):
            raise ValueError(
                f"pyarrow_dtype ({pyarrow_dtype}) must be an instance "
                f"of a pyarrow.DataType. Got {type(pyarrow_dtype)} instead."
            )
        self.pyarrow_dtype = pyarrow_dtype
