def returns_type(rs: Sequence[Return]) -> CType:
    if len(rs) == 0:
        return BaseCType(voidT)
    elif len(rs) == 1:
        return return_type(rs[0])
    else:
        return TupleCType([return_type(r) for r in rs])
