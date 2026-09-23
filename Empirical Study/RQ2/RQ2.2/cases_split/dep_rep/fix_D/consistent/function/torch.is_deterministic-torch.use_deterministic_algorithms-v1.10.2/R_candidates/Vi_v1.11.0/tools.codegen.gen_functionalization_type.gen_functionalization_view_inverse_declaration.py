@with_native_function
def gen_functionalization_view_inverse_declaration(f: NativeFunction) -> Optional[str]:
    # We only need to generate view_inverse declarations for view ops that:
    # - aren't composite (since they'll decompose and we'll get them for free).
    # - aren't inplace (since they should have a corresponding functional version, which we call instead).
    if f.is_view_op and not f.has_composite_implicit_autograd_kernel and not modifies_arguments(f):
        output = emit_declaration_for_noncomposite_views(f)
        return output
    return None
