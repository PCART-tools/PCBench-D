def gen_source_files(
        *,
        native_functions: Sequence[NativeFunction],
        grouped_native_functions: Sequence[Union[NativeFunction, NativeFunctionsGroup]],
        static_dispatch_idx: Optional[BackendIndex],
        selector: SelectiveBuilder,
        backend_indices: Dict[DispatchKey, BackendIndex],
        core_fm: FileManager,
        cpu_fm: FileManager,
        cuda_fm: FileManager,
        dispatch_keys: Sequence[DispatchKey],
        functions_keys: Set[DispatchKey],
        rocm: bool,
        force_schema_registration: bool,
        per_operator_headers: bool,
) -> None:
    extra_cuda_headers = '''\
#include <c10/cuda/CUDAGuard.h>
#include <ATen/cuda/ATenCUDAGeneral.h>
#include <ATen/cuda/CUDADevice.h>
#include <ATen/cuda/CUDAContext.h>'''
    if rocm:
        extra_cuda_headers = '''\
#include <ATen/hip/impl/HIPGuardImplMasqueradingAsCUDA.h>
#include <ATen/hip/ATenHIPGeneral.h>
#include <ATen/hip/HIPDevice.h>
#include <ATen/hip/HIPContext.h>'''

    for dispatch_key in dispatch_keys:
        fm = cuda_fm if is_cuda_dispatch_key(dispatch_key) else cpu_fm

        if per_operator_headers:
            def operator_headers() -> List[str]:
                headers = []
                for fn in native_functions:
                    is_registered = backend_index.has_kernel(fn) or (
                        fn.structured and dispatch_key in
                        (DispatchKey.Meta, DispatchKey.CompositeExplicitAutograd))
                    if not is_registered:
                        continue

                    headers.append(f"#include <ATen/ops/{fn.root_name}_native.h>")
                    if dispatch_key == DispatchKey.CompositeExplicitAutograd:
                        headers.append(f"#include <ATen/ops/{fn.root_name}.h>")
                    if dispatch_key in functions_keys:
                        headers.append(
                            f"#include <ATen/ops/{fn.root_name}_{dispatch_namespace}_dispatch.h>")

                return sorted(set(headers))
        else:
            def operator_headers() -> List[str]:
                headers = ["#include <ATen/NativeFunctions.h>"]
                if dispatch_key == DispatchKey.CompositeExplicitAutograd:
                    headers.append("#include <ATen/Functions.h>")
                if dispatch_key in functions_keys:
                    headers.append(f"#include <ATen/{dispatch_key!s}Functions.h>")
                return headers

        backend_index = backend_indices[dispatch_key]
        dispatch_namespace = str(dispatch_key).lower()
        fm.write_with_template(f'Register{dispatch_key}.cpp', 'RegisterDispatchKey.cpp', lambda: {
            'extra_cuda_headers': extra_cuda_headers if is_cuda_dispatch_key(dispatch_key) else '',
            'external_backend_headers': '',
            'dispatch_headers': dest.gen_registration_headers(backend_index, per_operator_headers),
            'ops_headers': operator_headers(),
            'DispatchKey': dispatch_key,
            'dispatch_namespace': dispatch_key.lower(),
            'dispatch_helpers': dest.gen_registration_helpers(backend_index),
            'dispatch_namespaced_definitions': list(concatMap(
                dest.RegisterDispatchKey(
                    backend_index,
                    Target.NAMESPACED_DEFINITION,
                    selector,
                    rocm=rocm,
                    cpp_namespace='at::native',
                    class_method_name=None),
                grouped_native_functions
            )),
            'dispatch_anonymous_definitions': list(concatMap(
                dest.RegisterDispatchKey(
                    backend_index,
                    Target.ANONYMOUS_DEFINITION,
                    selector,
                    rocm=rocm,
                    cpp_namespace='at::native',
                    class_method_name=None),
                grouped_native_functions
            )),
            'dispatch_registrations': list(concatMap(
                dest.RegisterDispatchKey(
                    backend_index,
                    Target.REGISTRATION,
                    selector,
                    rocm=rocm,
                    cpp_namespace='at::native',
                    class_method_name=None),
                grouped_native_functions
            )),
        })

    # BackendSelect is generated specially
    def gen_backend_select() -> Dict[str, List[str]]:
        relevant_fns = [fn for fn in native_functions if needs_backend_select(fn, selector)]
        return {
            'ops_headers': [f'#include <ATen/ops/{fn.root_name}_ops.h>' for fn in relevant_fns],
            'backend_select_method_definitions':
                list(mapMaybe(ComputeBackendSelect(Target.DEFINITION, selector), relevant_fns)),
            'backend_select_function_registrations':
                list(mapMaybe(ComputeBackendSelect(Target.REGISTRATION, selector), relevant_fns)),
        }
    cpu_fm.write('RegisterBackendSelect.cpp', gen_backend_select)

    schema_selector = selector
    if force_schema_registration:
        schema_selector = SelectiveBuilder.get_nop_selector()
    cpu_fm.write('RegisterSchema.cpp', lambda: {
        'schema_registrations': list(mapMaybe(RegisterSchema(schema_selector), native_functions)),
    })

    def key_func(fn: Union[NativeFunction, NativeFunctionsGroup]) -> str:
        return fn.root_name

    cpu_fm.write_sharded(
        'Operators.cpp',
        native_functions,
        key_fn=key_func,
        env_callable=lambda fn: {
            'operator_headers': [f'#include <ATen/ops/{fn.root_name}.h>'],
            'definitions': [ComputeOperators(Target.DEFINITION)(fn)]},
        num_shards=5,
        sharded_keys={'operator_headers', 'definitions'}
    )

    cpu_fm.write('Functions.cpp', lambda: {})

    core_fm.write('TensorMethods.cpp', lambda: {})

    core_fm.write('ATenOpList.cpp', lambda: {
        'aten_ops': list(mapMaybe(compute_aten_op, native_functions)),
    })

    # We need to easily map from [inplace_op_name] -> [functional_op] for the functionalization pass,
    # so here I generate a mapping from every operator name to its corresponding functional NativeFunction (if it exist).
    pre_grouped_d: Dict[FunctionSchema, Dict[SchemaKind, NativeFunction]] = pre_group_native_functions(native_functions)
    to_functional_op: Dict[OperatorName, Optional[NativeFunction]] = {
        k: v for d in [
            {f.func.name: pre_grouped_d[func][SchemaKind.functional]
                if SchemaKind.functional in pre_grouped_d[func].keys() else None
                for f in pre_grouped_d[func].values()}
            for func in pre_grouped_d.keys()]
        for k, v in d.items()
    }


    def functionalization_env_callable(
            g: Union[NativeFunction, NativeFunctionsGroup]
    ) -> Dict[str, List[str]]:
        functions = [g] if isinstance(g, NativeFunction) else list(g.functions())
        functions_needing_functionalization = [
            fn for fn in functions if needs_functionalization(selector, fn)]
        return {
            'ops_headers': ([
                f"#include <ATen/ops/{functions[0].root_name}_native.h>",
                f"#include <ATen/ops/{functions[0].root_name}_ops.h>",
            ] if functions_needing_functionalization else []),
            'func_definitions': list(mapMaybe(
                lambda f: gen_functionalization_definition(selector, f, to_functional_op[f.func.name]),
                functions_needing_functionalization)),
            'func_registrations': list(mapMaybe(
                lambda f: gen_functionalization_registration(
                    selector, f, backend_indices[DispatchKey.CompositeImplicitAutograd]),
                functions_needing_functionalization)),
        }


    cpu_fm.write_sharded(
        'RegisterFunctionalization.cpp',
        grouped_native_functions,
        key_fn=key_func,
        env_callable=functionalization_env_callable,
        num_shards=4,
        sharded_keys={'ops_headers', 'func_definitions', 'func_registrations'}
    )
