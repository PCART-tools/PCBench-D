def _create_named_tuple(t, unqual_name: str, field_names: List[str], defaults: Tuple[Any, ...]):
    # mypy: namedtuple() expects a string literal as the first argument
    if sys.version_info < (3, 7, 0):
        TupleType = collections.namedtuple(unqual_name, field_names)  # type: ignore[no-redef, misc]
        TupleType.__new__.__defaults__ = defaults    # type: ignore[attr-defined]
    else:
        TupleType = collections.namedtuple(unqual_name, field_names, defaults=defaults)  # type: ignore[call-arg, no-redef, misc]
    return TupleType(*t)
