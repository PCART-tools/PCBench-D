    def __arrow_c_array__(
        self, requested_schema: "PyCapsule" = None  # type: ignore[name-defined]  # noqa: F821, UP037
    ) -> tuple["PyCapsule", "PyCapsule"]:  # type: ignore[name-defined]  # noqa: F821, UP037
        raise NotImplementedError()
