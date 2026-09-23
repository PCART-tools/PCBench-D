def argumenttype_type(t: Type, *, mutable: bool, binds: ArgName) -> NamedCType:
    # If it's a value type, do the value type translation
    r = valuetype_type(t, binds=binds)
    if r is not None:
        return r

    if isinstance(t, BaseType):
        if t.name == BaseTy.Tensor:
            if mutable and not local.use_const_ref_for_mutable_tensors():
                return NamedCType(binds, MutRefCType(BaseCType(tensorT)))
            else:
                return NamedCType(binds, ConstRefCType(BaseCType(tensorT)))
        elif t.name == BaseTy.Scalar:
            return NamedCType(binds, ConstRefCType(BaseCType(scalarT)))
        else:
            raise AssertionError(f"base type should have been value type {t}")
    elif isinstance(t, OptionalType):
        if str(t.elem) == 'Tensor':
            if mutable and not local.use_const_ref_for_mutable_tensors():
                return NamedCType(binds, MutRefCType(BaseCType(tensorT)))  # TODO: fix this discrepancy
            else:
                return NamedCType(binds, ConstRefCType(OptionalCType(BaseCType(tensorT))))
        elif str(t.elem) == 'Scalar':
            return NamedCType(binds, ConstRefCType(OptionalCType(BaseCType(scalarT))))
        elem = argumenttype_type(t.elem, mutable=mutable, binds=binds)
        return NamedCType(binds, OptionalCType(elem.type))
    elif isinstance(t, ListType):
        # TODO: remove these special cases, ArrayRef fallthrough works fine
        if str(t.elem) == 'int':
            return NamedCType(binds, BaseCType(intArrayRefT))
        elif str(t.elem) == 'Tensor':
            return NamedCType(binds, BaseCType(tensorListT))
        elif str(t.elem) == 'Scalar':
            return NamedCType(binds, ArrayRefCType(BaseCType(scalarT)))
        elif str(t.elem) == 'Dimname':
            return NamedCType(binds, BaseCType(dimnameListT))
        elif str(t.elem) == 'Tensor?':
            return NamedCType(binds, ConstRefCType(ListCType(OptionalCType(BaseCType(tensorT)))))
        elem = argumenttype_type(t.elem, mutable=mutable, binds=binds)
        return NamedCType(binds, ArrayRefCType(elem.type))
    else:
        raise AssertionError(f"unrecognized type {repr(t)}")
