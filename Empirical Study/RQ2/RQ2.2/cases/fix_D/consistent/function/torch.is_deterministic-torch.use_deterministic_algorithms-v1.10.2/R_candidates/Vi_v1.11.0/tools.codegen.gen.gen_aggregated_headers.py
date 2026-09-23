def gen_aggregated_headers(
        *,
        native_functions: Sequence[NativeFunction],
        grouped_native_functions: Sequence[Union[NativeFunction, NativeFunctionsGroup]],
        static_dispatch_idx: Optional[BackendIndex],
        selector: SelectiveBuilder,
        backend_indices: Dict[DispatchKey, BackendIndex],
        cpu_fm: FileManager,
        cuda_fm: FileManager,
        functions_keys: Set[DispatchKey],
        dispatch_keys: Sequence[DispatchKey],
        rocm: bool,
) -> None:
    # Buck doesn't support dynamic output files, so we aggregate all operator
    # headers into a single file
    structured_native_functions = [g for g in grouped_native_functions
                                   if isinstance(g, NativeFunctionsGroup)]
    cpu_fm.write('NativeMetaFunctions.h', lambda: {
        'NativeMetaFunctions_includes': [],
        'NativeMetaFunctions_declarations': list(
            mapMaybe(compute_meta_function_declaration, structured_native_functions)),
    })
    method_native_functions = [fn for fn in native_functions
                               if Variant.method in fn.variants]
    non_method_native_functions = [fn for fn in native_functions
                                   if fn not in method_native_functions]
    cpu_fm.write('MethodOperators.h', lambda: {
        'MethodOperators_includes': [],
        'MethodOperators_declarations': list(mapMaybe(ComputeOperators(
            Target.DECLARATION), method_native_functions)),
    })
    cpu_fm.write('Operators.h', lambda: {
        'Operators_includes': ['#include <ATen/MethodOperators.h>'],
        'Operators_declarations': list(mapMaybe(ComputeOperators(
            Target.DECLARATION), non_method_native_functions)),
    })
    cpu_fm.write('Functions.h', lambda: {
        'static_dispatch_extra_headers': static_dispatch_extra_headers(static_dispatch_idx),
        'Functions_includes': ['#include <ATen/Operators.h>'],
        'Functions_declarations': list(mapMaybe(ComputeFunction(
            static_dispatch_backend_index=static_dispatch_idx), native_functions)),
    })
    cpu_fm.write('NativeFunctions.h', lambda: {
        'NativeFunctions_includes': ['#include <ATen/NativeMetaFunctions.h>'],
        'NativeFunctions_declarations': list(concatMap(
            # Convert to a set first to remove duplicate kernel names.
            # Backends are allowed to repeat kernel names; only generate the declaration once!
            lambda f: list(OrderedDict.fromkeys(concatMap(
                lambda backend_idx:
                    dest.compute_native_function_declaration(f, backend_idx),
                backend_indices.values()))),
            grouped_native_functions)),
    })

    for dispatch_key in dispatch_keys:
        fm = cuda_fm if is_cuda_dispatch_key(dispatch_key) else cpu_fm
        if dispatch_key in functions_keys:
            if dispatch_key in static_dispatch_keys(static_dispatch_idx):
                # See Note [Avoiding Include Cycles In Static Dispatch]
                inl_headers = ''
            else:
                inl_headers = f'#include <ATen/{dispatch_key}Functions_inl.h>'

            fm.write_with_template(f'{dispatch_key}Functions.h', 'DispatchKeyFunctions.h', lambda: {
                'dispatch_key': str(dispatch_key),
                'inline_headers_for_nonstatic_build': inl_headers,
            })
            fm.write_with_template(f'{dispatch_key}Functions_inl.h', 'DispatchKeyFunctions_inl.h', lambda: {
                'DispatchKeyFunctions_inl_includes': [],
                'dispatch_namespace': dispatch_key.lower(),
                'dispatch_namespaced_declarations': list(concatMap(
                    dest.RegisterDispatchKey(
                        backend_indices[dispatch_key],
                        Target.NAMESPACED_DECLARATION,
                        selector,
                        rocm=rocm,
                        cpp_namespace='at::native',
                        class_method_name=None),
                    grouped_native_functions
                )),
            })

        del fm
