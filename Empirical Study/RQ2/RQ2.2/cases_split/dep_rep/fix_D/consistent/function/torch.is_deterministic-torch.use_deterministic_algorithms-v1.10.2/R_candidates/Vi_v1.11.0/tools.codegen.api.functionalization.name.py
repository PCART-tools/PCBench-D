def name(f: NativeFunction, *, functional_op: NativeFunction, is_reverse: bool, include_namespace: bool) -> str:
    # For inplace_view ops, the lambda calls out to the corresponding functional view op
    fn = functional_op if f.tag is Tag.inplace_view else f
    name = fn.func.name.unambiguous_name()
    if is_reverse:
        # in the reverse case, we codegen both the call-sites (which need the full namespace) and the declarations (which don't)
        if include_namespace:
            return f'at::functionalization::FunctionalInverses::{name}_inverse'
        else:
            return f'{name}_inverse'
    # in the forward case, we just diretly call into the at::_ops API (so we always need the namespace)
    assert include_namespace
    return f'at::_ops::{name}::call'
