@deprecated(
    "`is_namedtuple` is deprecated, please use the python checks instead",
    category=FutureWarning,
)
def is_namedtuple(obj: Any) -> bool:
    # Check if type was created from collections.namedtuple or a typing.NamedTuple.
    return _is_namedtuple(obj)
