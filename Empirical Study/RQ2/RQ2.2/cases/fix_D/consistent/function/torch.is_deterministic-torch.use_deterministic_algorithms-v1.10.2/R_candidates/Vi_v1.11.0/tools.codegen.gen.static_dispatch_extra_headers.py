def static_dispatch_extra_headers(backend: Optional[BackendIndex], skip_tensor_include: bool = False) -> List[str]:
    if skip_tensor_include:
        # See Note [Avoiding Include Cycles In Static Dispatch]
        maybe_inl = '_inl'
    else:
        maybe_inl = ''
    return [f'#include <ATen/{dispatch_key}Functions{maybe_inl}.h>'
            for dispatch_key in static_dispatch_keys(backend)]
