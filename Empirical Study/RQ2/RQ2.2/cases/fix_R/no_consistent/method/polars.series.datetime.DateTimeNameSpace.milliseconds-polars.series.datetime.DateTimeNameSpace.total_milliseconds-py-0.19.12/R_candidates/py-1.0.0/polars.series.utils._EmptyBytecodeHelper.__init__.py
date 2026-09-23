    def __init__(self) -> None:
        # generate bytecode for empty functions with/without a docstring
        def _empty_with_docstring() -> None:
            """"""  # noqa: D419

        def _empty_without_docstring() -> None:
            pass

        self.empty_bytecode = (
            _empty_with_docstring.__code__.co_code,
            _empty_without_docstring.__code__.co_code,
        )
