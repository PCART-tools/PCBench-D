@with_native_function_with_differentiability_info
def inplace_or_view_method_registration(fn: NativeFunctionWithDifferentiabilityInfo) -> Optional[str]:
    f = fn.func
    if get_view_info(f) is None and (not modifies_arguments(f) or is_foreach_op(str(f.func.name))):
        return None
    return WRAPPER_REGISTRATION.substitute(
        unqual_operator_name_with_overload=f.func.name,
        type_wrapper_name=type_wrapper_name(f),
        class_type='ADInplaceOrView',
    )
