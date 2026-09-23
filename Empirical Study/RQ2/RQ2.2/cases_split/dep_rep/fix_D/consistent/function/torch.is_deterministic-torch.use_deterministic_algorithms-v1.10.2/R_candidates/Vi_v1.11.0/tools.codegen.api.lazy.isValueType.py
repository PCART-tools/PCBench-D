def isValueType(typ: Union[Type, BaseCType, OptionalCType, ConstRefCType, MutRefCType,
                           ListCType, ArrayRefCType, ArrayCType, VectorCType, TupleCType]) -> bool:
    """
    Given a type, determine if it is a Value-like type.  This is equivalent to
    being Tensor-like, but assumes the type has already been transformed.
    """
    if isinstance(typ, BaseCType):
        return typ.type == valueT
    elif isinstance(typ, (OptionalCType, ListCType, VectorCType)):
        return isValueType(typ.elem)
    else:
        return False
