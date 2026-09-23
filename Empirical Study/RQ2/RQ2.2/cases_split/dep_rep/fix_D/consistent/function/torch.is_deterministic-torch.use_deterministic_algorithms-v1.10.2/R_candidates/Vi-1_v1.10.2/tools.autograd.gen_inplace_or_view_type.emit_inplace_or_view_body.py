@with_native_function_with_differentiability_info
def emit_inplace_or_view_body(fn: NativeFunctionWithDifferentiabilityInfo) -> List[str]:
    f = fn.func
    inplace_view_body: List[str] = []

    dispatcher_sig = DispatcherSignature.from_schema(f.func)
    dispatcher_exprs = dispatcher_sig.exprs()

    # code-generated ADInplaceOrView kernels plumb and recompute dispatch keys directly through the kernel for performance.
    # See Note [Plumbing Keys Through The Dispatcher] for details.
    dispatch_key_set = 'ks & c10::after_ADInplaceOrView_keyset'
    redispatch_args = ', '.join([dispatch_key_set] + [a.expr for a in dispatcher_exprs])

    # Note that this calls the slow, dispatching variants of manual_cpp_binding ops.
    # We could probably work harder to ensure that the fast variants are called instead, but the perf benefit would be minimal.
    sig_group = CppSignatureGroup.from_native_function(f, method=False, fallback_binding=f.manual_cpp_binding)
    if sig_group.faithful_signature is not None:
        api_name = sig_group.faithful_signature.name()
    else:
        api_name = sig_group.signature.name()
    if modifies_arguments(f):  # inplace op
        inplace_view_body.append(INPLACE_REDISPATCH.substitute(
            api_name=api_name,
            unpacked_args=redispatch_args,
        ))
        for r in cpp.return_names(f):
            inplace_view_body.append(f'increment_version({r});')
    else:
        assert(get_view_info(fn) is not None)
        inplace_view_body.append(VIEW_REDISPATCH.substitute(
            assign_return_values='auto ' + TMP_VAR + ' = ',
            api_name=api_name,
            unpacked_args=redispatch_args,
        ))
        call, rhs_value = emit_view_body(fn, TMP_VAR)
        inplace_view_body.append(call)
        assert rhs_value is not None
        inplace_view_body.append(
            ASSIGN_RETURN_VALUE.substitute(return_values=tie_return_values(f), rhs_value=rhs_value))
    if f.func.returns:
        inplace_view_body.append(f'return {get_return_value(f)};')
    return inplace_view_body
