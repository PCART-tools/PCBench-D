def gen_dispatcher_registrations(
        fm: FileManager,
        output_dir: str,
        cpp_namespace: str,
        backend_indices: Dict[DispatchKey, BackendIndex],
        grouped_native_functions: Sequence[Union[NativeFunction, NativeFunctionsGroup]],
        backend_dispatch_key: DispatchKey,
        dispatch_key: DispatchKey,
        selector: 'SelectiveBuilder') -> None:
    backend_index = backend_indices[dispatch_key]
    fm.write_with_template(f'Register{dispatch_key}.cpp', 'RegisterDispatchKey.cpp', lambda: {
        'extra_cuda_headers': '',
        'external_backend_headers': f'#include "{output_dir}/{backend_dispatch_key}NativeFunctions.h"',
        'ops_headers': '#include <ATen/Functions.h>',
        'DispatchKey': dispatch_key,
        'dispatch_namespace': dispatch_key.lower(),
        'dispatch_headers': dest.gen_registration_headers(backend_index, per_operator_headers=False),
        'dispatch_helpers': dest.gen_registration_helpers(backend_index),
        'dispatch_namespaced_definitions': list(concatMap(
            dest.RegisterDispatchKey(
                backend_index,
                Target.NAMESPACED_DEFINITION,
                selector,
                rocm=False,
                cpp_namespace=cpp_namespace,
                class_method_name=f'{backend_dispatch_key}NativeFunctions'),
            grouped_native_functions
        )),
        'dispatch_anonymous_definitions': list(concatMap(
            dest.RegisterDispatchKey(
                backend_index,
                Target.ANONYMOUS_DEFINITION,
                selector,
                rocm=False,
                cpp_namespace=cpp_namespace,
                class_method_name=f'{backend_dispatch_key}NativeFunctions'),
            grouped_native_functions
        )),
        'dispatch_registrations': list(concatMap(
            dest.RegisterDispatchKey(
                backend_index,
                Target.REGISTRATION,
                selector,
                rocm=False,
                cpp_namespace=cpp_namespace,
                class_method_name=f'{dispatch_key}NativeFunctions'),
            grouped_native_functions
        )),
    })
