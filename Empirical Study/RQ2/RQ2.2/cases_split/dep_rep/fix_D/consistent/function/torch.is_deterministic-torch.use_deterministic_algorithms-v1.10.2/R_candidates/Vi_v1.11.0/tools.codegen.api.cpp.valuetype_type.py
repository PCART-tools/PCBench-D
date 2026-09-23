def valuetype_type(t: Type, *, binds: ArgName, remove_non_owning_ref_types: bool = False) -> Optional[NamedCType]:
    if isinstance(t, BaseType):
        if t.name == BaseTy.Tensor or t.name == BaseTy.Scalar:
            return None
        if remove_non_owning_ref_types:
            if t.name == BaseTy.str:
                raise AssertionError("string ref->value conversion: not implemented yet")
        # All other BaseType currently map directly to BaseCppTypes.
        return NamedCType(binds, BaseCType(BaseTypeToCppMapping[t.name]))
    elif isinstance(t, OptionalType):
        elem = valuetype_type(t.elem, binds=binds)
        if elem is None:
            return None
        return NamedCType(binds, OptionalCType(elem.type))
    elif isinstance(t, ListType):
        if str(t.elem) == 'bool':
            assert t.size is not None
            return NamedCType(binds, ArrayCType(BaseCType(boolT), t.size))
        else:
            return None
    else:
        raise AssertionError(f"unrecognized type {repr(t)}")
