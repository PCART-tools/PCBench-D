def node_ctor_arg_rvalue_string(arg: NamedCType) -> str:
    """
    Given a NamedCType from a lazy IR schema,
    generate a c++ string for materializing an rvalue of that arg for passing into
    a lazy Node constructor.
    """
    if isValueType(arg.type):
        if isinstance(arg.type, BaseCType):
            return f"lazy_{arg.name}.GetIrValue()"
        elif isinstance(arg.type, OptionalCType):
            return f"lazy_{arg.name} ? " \
                   f"c10::make_optional(lazy_{arg.name}.GetIrValue()) : " \
                   "c10::nullopt"
        else:
            raise AssertionError("TODO not sure if there are other valid types to handle here")
    else:
        if isinstance(arg.type, VectorCType) and isinstance(arg.type.elem, BaseCType):
            return f"std::vector<{arg.type.elem.type}>({arg.name}.begin(), {arg.name}.end())"
        elif (isinstance(arg.type, OptionalCType) and
                isinstance(arg.type.elem, VectorCType) and
                isinstance(arg.type.elem.elem, BaseCType)):
            return f"torch::lazy::ToOptionalVector<{arg.type.elem.elem.type}>({arg.name})"
        else:
            return f"{arg.name}"
