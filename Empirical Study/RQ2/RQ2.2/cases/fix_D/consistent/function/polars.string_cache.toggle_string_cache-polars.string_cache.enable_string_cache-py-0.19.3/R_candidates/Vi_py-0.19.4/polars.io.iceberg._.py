@_convert_predicate.register(List)
def _(a: List) -> Any:
    return [_convert_predicate(e) for e in a.elts]
