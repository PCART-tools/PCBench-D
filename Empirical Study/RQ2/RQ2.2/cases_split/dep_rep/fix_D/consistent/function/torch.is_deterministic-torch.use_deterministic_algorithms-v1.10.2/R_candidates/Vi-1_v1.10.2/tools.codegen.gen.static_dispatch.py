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

    if f.structured_delegate is not None:
        # TODO: for ops with structured_delegate it should check the dispatch table of
        # the out variant instead. For now, these structured ops all have CPU/CUDA kernels
        # so we always dispatch to the `backend`, but this could be wrong when we
        # migrate math/default_backend ops to use structured delegate.
        return f'return at::{backend_index.dispatch_key.lower()}::{name}({exprs_str});'

    if backend_index.has_kernel(f):
        return f'return at::{backend_index.dispatch_key.lower()}::{name}({exprs_str});'
    elif f.has_composite_explicit_autograd_kernel:
        return f'return at::{DispatchKey.CompositeExplicitAutograd.lower()}::{name}({exprs_str});'
    elif f.has_composite_implicit_autograd_kernel:
        return f'return at::{DispatchKey.CompositeImplicitAutograd.lower()}::{name}({exprs_str});'

    return f'TORCH_CHECK(false, "Static dispatch does not support {name} for {backend_index.dispatch_key}.");'
