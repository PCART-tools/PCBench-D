def argument_type(a: Argument, *, binds: ArgName, remove_non_owning_ref_types: bool = False) -> NamedCType:
    return argumenttype_type(a.type, mutable=a.is_write, binds=binds, remove_non_owning_ref_types=remove_non_owning_ref_types)
