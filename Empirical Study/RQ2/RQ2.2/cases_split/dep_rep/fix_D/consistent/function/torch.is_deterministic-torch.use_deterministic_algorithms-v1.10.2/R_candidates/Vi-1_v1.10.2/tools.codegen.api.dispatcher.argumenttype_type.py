def argumenttype_type(t: Type, *, mutable: bool, binds: ArgName) -> NamedCType:
    # This is a faux amis.  If it makes sense in the future to add
    # more special cases here, or invert things so cpp.argument_type
    # calls this, or just completely inline the function, please do
    # it.
    return cpp.argumenttype_type(t, mutable=mutable, binds=binds)
