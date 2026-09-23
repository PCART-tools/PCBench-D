@with_native_function_with_differentiability_info
def inplace_or_view_method_definition(fn: NativeFunctionWithDifferentiabilityInfo) -> Optional[str]:
    f = fn.func
    if get_view_info(f) is None and (not modifies_arguments(f) or is_foreach_op(str(f.func.name))):
        return None
    return METHOD_DEFINITION.substitute(
        return_type=cpp.returns_type(f.func.returns).cpp_type(),
        type_wrapper_name=type_wrapper_name(f),
        formals=gen_formals(f),
        type_definition_body=emit_inplace_or_view_body(fn),
    )
