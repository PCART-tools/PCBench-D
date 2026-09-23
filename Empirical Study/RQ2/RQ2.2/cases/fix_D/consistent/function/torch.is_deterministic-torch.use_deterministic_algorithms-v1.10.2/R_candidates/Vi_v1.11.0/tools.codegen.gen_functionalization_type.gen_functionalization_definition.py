def gen_functionalization_definition(
    selector: SelectiveBuilder,
    f: NativeFunction,
    functional_op: Optional[NativeFunction]
) -> Optional[str]:
    @with_native_function
    def emit_definition_helper(f: NativeFunction) -> Optional[str]:
        if not needs_functionalization(selector, f):
            return None
        if f.is_view_op and f.has_composite_implicit_autograd_kernel:
            # See Note [Composite view ops in the functionalization pass]
            return None
        # order is important here, ops that are both views and mutations should hit the view path.
        if f.is_view_op:
            # Every view op is expected to have a functional counterpart (e.g. transpose_() -> transpose())
            assert functional_op is not None
            body_str = emit_view_functionalization_body(f, functional_op)
        else:
            # inplace op
            assert modifies_arguments(f)
            body_str = emit_inplace_functionalization_body(f, functional_op)
        sig = DispatcherSignature.from_schema(f.func)
        return f"""
    {sig.defn(name=wrapper_name(f.func), is_redispatching_fn=True)} {{
    {body_str}
    }}
    """

    return emit_definition_helper(f)
