def _checked_cast(ty: type[_T], obj: object) -> _T:
    assert isinstance(obj, ty), f"expected {ty} but got {type(obj)}"
    return obj
