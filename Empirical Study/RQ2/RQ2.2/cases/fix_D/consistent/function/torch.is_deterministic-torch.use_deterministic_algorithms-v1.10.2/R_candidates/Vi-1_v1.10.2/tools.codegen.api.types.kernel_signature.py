def kernel_signature(
        f: NativeFunction, backend_index: BackendIndex, *, prefix: str = '') -> Union['NativeSignature', 'DispatcherSignature']:
    # Note [External Backends Follow Dispatcher API]
    # Kernel signatures for in-tree backends follow the "native" API,
    # while kernels for out-of-tree backends follow the dispatcher API.
    # See the comments in `native.py` for details, but historically there have been
    # some small differences in schema convention between them and the Dispatcher API.
    # Any differences that require translating between the two will results in a runtime cost,
    # so we'd like to keep the differences as small as possible.
    # With external backends, we'd like to enforce that they write their kernels with schemas
    # that match the Dispatcher API directly, if they can.
    if backend_index.external:
        return DispatcherSignature.from_schema(f.func, prefix=prefix)
    else:
        return NativeSignature(f.func, prefix)
