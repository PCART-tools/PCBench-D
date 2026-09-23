    def __init__(self, storage=None) -> None:
        if storage is None:
            infer_string = get_option("future.infer_string")
            if infer_string:
                storage = "pyarrow_numpy"
            else:
                storage = get_option("mode.string_storage")
        if storage not in {"python", "pyarrow", "pyarrow_numpy"}:
            raise ValueError(
                f"Storage must be 'python' or 'pyarrow'. Got {storage} instead."
            )
        if storage in ("pyarrow", "pyarrow_numpy") and pa_version_under7p0:
            raise ImportError(
                "pyarrow>=7.0.0 is required for PyArrow backed StringArray."
            )
        self.storage = storage
