def gen_registration_headers(
        backend_index: BackendIndex,
        per_operator_headers: bool,
) -> List[str]:
    if per_operator_headers:
        headers = ["#include <ATen/ops/as_strided_native.h>"]
    else:
        headers = ["#include <ATen/NativeFunctions.h>"]

    if backend_index.dispatch_key in (DispatchKey.CPU, DispatchKey.Meta):
        headers.append("#include <ATen/EmptyTensor.h>")
    elif backend_index.dispatch_key == DispatchKey.CUDA:
        headers.append("#include <ATen/cuda/EmptyTensor.h>")
    elif per_operator_headers:
        headers += [
            "#include <ATen/ops/empty.h>",
            "#include <ATen/ops/empty_strided.h>"]
    else:
        headers.append("#include <ATen/Functions.h>")

    return headers
