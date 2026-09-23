def cpp_dispatch_exprs(f: NativeFunction, *,
                       python_signature: Optional[PythonSignature] = None,
                       ) -> Tuple[str, ...]:
    cpp_args: Sequence[Binding] = _cpp_signature(f, method=False).arguments()

    exprs: Tuple[str, ...] = tuple()
    if not isinstance(python_signature, PythonSignatureDeprecated):
        # By default the exprs are consistent with the C++ signature.
        exprs = tuple(map(lambda a: a.name, cpp_args))
    else:
        # For deprecated python signature we may need fill in some constants.
        exprs = tuple(filter(lambda n: n != 'out' or f.func.is_out_fn(),
                             python_signature.deprecated_args_exprs))

    if Variant.method in f.variants:
        exprs = tuple(filter('self'.__ne__, exprs))

    return exprs
