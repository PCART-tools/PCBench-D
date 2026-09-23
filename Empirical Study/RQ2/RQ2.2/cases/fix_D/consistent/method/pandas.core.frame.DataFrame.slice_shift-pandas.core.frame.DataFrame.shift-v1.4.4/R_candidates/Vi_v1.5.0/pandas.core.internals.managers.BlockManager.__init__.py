    def __init__(
        self,
        blocks: Sequence[Block],
        axes: Sequence[Index],
        refs: list[weakref.ref | None] | None = None,
        verify_integrity: bool = True,
    ) -> None:

        if verify_integrity:
            # Assertion disabled for performance
            # assert all(isinstance(x, Index) for x in axes)

            for block in blocks:
                if self.ndim != block.ndim:
                    raise AssertionError(
                        f"Number of Block dimensions ({block.ndim}) must equal "
                        f"number of axes ({self.ndim})"
                    )
                if isinstance(block, DatetimeTZBlock) and block.values.ndim == 1:
                    # TODO(2.0): remove once fastparquet no longer needs this
                    warnings.warn(
                        "In a future version, the BlockManager constructor "
                        "will assume that a DatetimeTZBlock with block.ndim==2 "
                        "has block.values.ndim == 2.",
                        DeprecationWarning,
                        stacklevel=find_stack_level(inspect.currentframe()),
                    )

                    # error: Incompatible types in assignment (expression has type
                    # "Union[ExtensionArray, ndarray]", variable has type
                    # "DatetimeArray")
                    block.values = ensure_block_shape(  # type: ignore[assignment]
                        block.values, self.ndim
                    )
                    try:
                        block._cache.clear()
                    except AttributeError:
                        # _cache not initialized
                        pass

            self._verify_integrity()
