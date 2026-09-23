def argumenttype_type(t: Type, *, mutable: bool, binds: ArgName) -> NamedCType:
    if str(t) == 'Tensor?':
        tensor_type: OptionalCType = OptionalCType(BaseCType(tensorT))
        if mutable and not local.use_const_ref_for_mutable_tensors():
            return NamedCType(binds, MutRefCType(tensor_type))
        else:
            return NamedCType(binds, ConstRefCType(tensor_type))
    elif str(t) == 'Tensor?[]':
        return NamedCType(binds, ConstRefCType(ListCType(OptionalCType(BaseCType(tensorT)))))
    elif str(t) == 'Scalar':
        return NamedCType(binds, ConstRefCType(BaseCType(scalarT)))
    elif str(t) == 'Scalar?':
        return NamedCType(binds, ConstRefCType(OptionalCType(BaseCType(scalarT))))
    return cpp.argumenttype_type(t, mutable=mutable, binds=binds)
