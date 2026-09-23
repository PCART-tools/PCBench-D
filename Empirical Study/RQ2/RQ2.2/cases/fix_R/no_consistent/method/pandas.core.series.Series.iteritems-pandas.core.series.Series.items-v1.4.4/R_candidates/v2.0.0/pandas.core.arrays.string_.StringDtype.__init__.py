    def __init__(self, storage=None) -> None:
        if storage is None:
            storage = get_option("mode.string_storage")
        if storage not in {"python", "pyarrow"}:
            raise ValueError(
                f"Storage must be 'python' or 'pyarrow'. Got {storage} instead."
            )
        if storage == "pyarrow" and pa_version_under7p0:
            raise ImportError(
                "pyarrow>=7.0.0 is required for PyArrow backed StringArray."
            )
        self.storage = storage
