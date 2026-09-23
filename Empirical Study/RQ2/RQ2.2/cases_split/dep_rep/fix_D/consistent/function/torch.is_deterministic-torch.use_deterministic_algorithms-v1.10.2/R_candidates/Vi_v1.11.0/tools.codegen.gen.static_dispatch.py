def static_dispatch(
    f: NativeFunction, cpp_sig: CppSignature,
    *, method: bool, backend_index: Optional[BackendIndex]
) -> Optional[str]:
    if backend_index is None or f.manual_kernel_registration:
        return None
    target_sig = CppSignatureGroup.from_native_function(f, method=False, fallback_binding=False).signature
    name = target_sig.name()
    exprs = translate(cpp_sig.arguments(), target_sig.arguments(), method=method)
    exprs_str = ', '.join(a.expr for a in exprs)

    dispatch_key = get_static_dispatch_backend(f, backend_index)
    if dispatch_key is not None:
        return f'return at::{dispatch_key.lower()}::{name}({exprs_str});'

    return f'TORCH_CHECK(false, "Static dispatch does not support {name} for {backend_index.dispatch_key}.");'
