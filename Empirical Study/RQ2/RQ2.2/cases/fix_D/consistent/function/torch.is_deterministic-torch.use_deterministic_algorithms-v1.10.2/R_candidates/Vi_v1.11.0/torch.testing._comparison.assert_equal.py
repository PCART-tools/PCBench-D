def assert_equal(
    actual: Any,
    expected: Any,
    *,
    pair_types: Sequence[Type[Pair]] = (ObjectPair,),
    sequence_types: Tuple[Type, ...] = (collections.abc.Sequence,),
    mapping_types: Tuple[Type, ...] = (collections.abc.Mapping,),
    **options: Any,
) -> None:
    """Asserts that inputs are equal.

    ``actual`` and ``expected`` can be possibly nested :class:`~collections.abc.Sequence`'s or
    :class:`~collections.abc.Mapping`'s. In this case the comparison happens elementwise by recursing through them.

    Args:
        actual (Any): Actual input.
        expected (Any): Expected input.
        pair_types (Sequence[Type[Pair]]): Sequence of :class:`Pair` types that will be tried to construct with the
            inputs. First successful pair will be used. Defaults to only using :class:`ObjectPair`.
        sequence_types (Tuple[Type, ...]): Optional types treated as sequences that will be checked elementwise.
        mapping_types (Tuple[Type, ...]): Optional types treated as mappings that will be checked elementwise.
        **options (Any): Options passed to each pair during construction.
    """
    # Hide this function from `pytest`'s traceback
    __tracebackhide__ = True

    try:
        pairs = originate_pairs(
            actual,
            expected,
            pair_types=pair_types,
            sequence_types=sequence_types,
            mapping_types=mapping_types,
            **options,
        )
    except ErrorMeta as error_meta:
        # Explicitly raising from None to hide the internal traceback
        raise error_meta.to_error() from None

    error_metas: List[ErrorMeta] = []
    for pair in pairs:
        try:
            pair.compare()
        except ErrorMeta as error_meta:
            error_metas.append(error_meta)
        # Raising any exception besides `ErrorMeta` while comparing is unexpected and will give some extra information
        # about what happened. If applicable, the exception should be expected in the future.
        except Exception as error:
            raise RuntimeError(
                f"Comparing\n\n"
                f"{pair}\n\n"
                f"resulted in the unexpected exception above. "
                f"If you are a user and see this message during normal operation "
                "please file an issue at https://github.com/pytorch/pytorch/issues. "
                "If you are a developer and working on the comparison functions, "
                "please except the previous error and raise an expressive `ErrorMeta` instead."
            ) from error

    if not error_metas:
        return

    # TODO: compose all metas into one AssertionError
    raise error_metas[0].to_error()
