def gen_trace_type_func(
    fn: NativeFunction
) -> Dict[str, List[str]]:
    return {
        'ops_headers': [f'#include <ATen/ops/{fn.root_name}_ops.h>'],
        'trace_method_definitions': [method_definition(fn)],
        'trace_wrapper_registrations': [method_registration(fn)],
    }
