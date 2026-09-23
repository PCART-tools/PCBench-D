def static_dispatch_ops_header(
        f: NativeFunction,
        backend_index: Optional[BackendIndex]) -> Optional[str]:
    if backend_index is None or f.manual_kernel_registration:
        return None

    dispatch_key = get_static_dispatch_backend(f, backend_index)
    return (f'#include <ATen/ops/{f.root_name}_{dispatch_key.lower()}_dispatch.h>'
            if dispatch_key is not None else None)
